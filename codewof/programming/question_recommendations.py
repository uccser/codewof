"""Question recommendations for codeWOF."""

import random
import statistics

from django.db.models import Q

from programming.models import DifficultyLevel, ProgrammingConcepts, QuestionContexts, Question
from programming.skill_and_level_tracking import get_level_and_skill_info


def get_recommendation_descriptions():
    """Get recommendation descriptions, using a (heading, details) format."""
    return (
        (
            'Want to maintain your skills?',
            'This question is likely to be at a difficulty you are accustomed to, while making use of a wide range of '
            'programming concepts and question contexts.'
        ),
        (
            'Are you up for a challenge?',
            'This question is at a higher difficulty level than what you are likely to be comfortable with, while '
            'utilising concepts and contexts you are well versed in.'
        ),
    )


def get_recommended_questions(profile):
    """Get the recommended questions based on the user's previously answered questions."""
    level_and_skill_info = get_level_and_skill_info(profile)
    scores = get_scores(level_and_skill_info)
    unsolved_questions = get_unsolved_questions(profile)
    recommended_questions = calculate_recommended_questions(scores, unsolved_questions)
    return recommended_questions


def get_scores(level_and_skill_info):
    """
    Return a dictionary of scores and numbers from the given tracked information.

    Creates scores based on all questions answered, and those answered within the past month.
    """
    difficulty_levels = sorted(list(set([difficulty.level for difficulty in DifficultyLevel.objects.all()])))
    concept_numbers = sorted(list(set([concept.number for concept in ProgrammingConcepts.objects.all()])))
    context_numbers = sorted(list(set([context.number for context in QuestionContexts.objects.all()])))
    return {
        'difficulty': {
            'all': generate_scores(difficulty_levels, level_and_skill_info['all']['difficulty_level']),
            'month': generate_scores(difficulty_levels, level_and_skill_info['month']['difficulty_level']),
            'numbers': difficulty_levels,
        },
        'concept': {
            'all': generate_scores(concept_numbers, level_and_skill_info['all']['concept_num']),
            'month': generate_scores(concept_numbers, level_and_skill_info['month']['concept_num']),
            'numbers': concept_numbers,
        },
        'context': {
            'all': generate_scores(context_numbers, level_and_skill_info['all']['context_num']),
            'month': generate_scores(context_numbers, level_and_skill_info['month']['context_num']),
            'numbers': context_numbers,
        },
    }


def generate_scores(numbers, info_category):
    """Generate and return the scores based on a given information category (e.g. difficulty)."""
    scores = [None] * len(numbers)
    for index, category_num in enumerate(numbers):
        if category_num in info_category:
            if scores[index] is None:
                scores[index] = 0
            scores[index] -= info_category[category_num]['num_solved']
            scores[index] += statistics.mean(info_category[category_num]['attempts']) - 1
    return scores


def get_unsolved_questions(profile):
    """Get all questions unsolved by the user."""
    return (
        Question.objects.all()
        .filter(
            Q(attempt__isnull=True) | (Q(attempt__passed_tests=False, attempt__profile=profile))
        )
        .distinct('pk')
        .select_subclasses()
        .select_related('difficulty_level')
        .prefetch_related(
            'concepts',
            'concepts__parent',
            'contexts',
            'contexts__parent',
        )
    )


def calculate_recommended_questions(scores, unsolved_questions):
    """
    Get the recommended questions from calculations based on the provided scores and user.

    Retrieves the recommendation values for the difficulty, concept, and context, and uses this to calculate the
    recommended questions.
    """
    comfortable_difficulty_questions, comfortable_concepts_contexts_questions = get_recommendation_categories(
        scores, unsolved_questions
    )
    recommended_questions = get_random_recommendations(
        comfortable_difficulty_questions, comfortable_concepts_contexts_questions
    )
    return recommended_questions


def get_recommendation_categories(scores, unsolved_questions):
    """Get the recommendations for all categories (comfortable difficulty, and comfortable concepts/contexts)."""
    comfortable_difficulties = get_comfortable_difficulties(scores['difficulty'])
    uncomfortable_concepts = get_uncomfortable_concepts_or_contexts(scores['concept'])
    uncomfortable_contexts = get_uncomfortable_concepts_or_contexts(scores['context'])
    comfortable_difficulty_recommendations = get_recommendations(
        unsolved_questions, comfortable_difficulties, uncomfortable_concepts, uncomfortable_contexts
    )
    uncomfortable_difficulties = get_uncomfortable_difficulties(
        comfortable_difficulties, scores['difficulty']['numbers']
    )
    comfortable_concepts = list(reversed(uncomfortable_concepts))
    comfortable_contexts = list(reversed(uncomfortable_contexts))
    comfortable_concepts_contexts_recommendations = get_recommendations(
        unsolved_questions, uncomfortable_difficulties, comfortable_concepts, comfortable_contexts
    )
    return comfortable_difficulty_recommendations, comfortable_concepts_contexts_recommendations


def get_recommendations(questions, ordered_difficulties, ordered_concepts, ordered_contexts):
    """
    Get the question recommendations for the given ordered difficulty, concepts, and contexts.

    Iterates through possible combinations to find valid questions that matches the criteria.
    """
    initial_concepts = ordered_concepts[0]
    for difficulty in ordered_difficulties:
        comfortable_difficulty_questions = questions.filter(difficulty_level__level=difficulty)
        for contexts in ordered_contexts:
            recommendations = calculate_comfortable_difficulty_questions(
                comfortable_difficulty_questions, initial_concepts, contexts
            )
            if len(recommendations) > 0:
                return recommendations
        for concepts in ordered_concepts:
            recommendations = calculate_comfortable_difficulty_questions(
                comfortable_difficulty_questions, concepts
            )
            if len(recommendations) > 0:
                return recommendations
        recommendations = calculate_comfortable_difficulty_questions(
            comfortable_difficulty_questions
        )
        if len(recommendations) > 0:
            return recommendations
    return []


def calculate_comfortable_difficulty_questions(questions, concepts=None, contexts=None):
    """Calculate and return the comfortable difficulty, uncomfortable concepts/contexts, question recommendations."""
    comfortable_difficulty_questions = []
    for question in questions:
        filters = []
        if concepts is not None:
            question_concepts = [concept.number for concept in question.concepts.all()]
            filters.append(
                any(concept in question_concepts for concept in concepts))
        if contexts is not None:
            question_contexts = [context.number for context in question.contexts.all()]
            filters.append(
                any(context in question_contexts for context in contexts))
        if all(filters):
            comfortable_difficulty_questions.append(question)
    return comfortable_difficulty_questions


def get_random_recommendations(comfortable_difficulty_questions, comfortable_concepts_contexts_questions):
    """Get a random (and unique) recommendation with questions from each recommendation category."""
    random_recommendations = []
    if len(comfortable_difficulty_questions) > 0:
        comfortable_difficulty_choice = random.choice(comfortable_difficulty_questions)
        random_recommendations.append(comfortable_difficulty_choice)
        if comfortable_difficulty_choice in comfortable_concepts_contexts_questions:
            comfortable_concepts_contexts_questions.remove(comfortable_difficulty_choice)
    if len(comfortable_concepts_contexts_questions) > 0:
        comfortable_concepts_contexts_choice = random.choice(comfortable_concepts_contexts_questions)
        random_recommendations.append(comfortable_concepts_contexts_choice)
    return random_recommendations


def get_comfortable_difficulties(scores):
    """Return comfortable difficulty levels (reasonable for the user to solve, not too hard or easy, in-order)."""
    comfortable_difficulty = calculate_comfortable_difficulties(scores['month'], scores['numbers'])
    if comfortable_difficulty is None:
        comfortable_difficulty = calculate_comfortable_difficulties(scores['all'], scores['numbers'])
    if comfortable_difficulty is None:
        comfortable_difficulty = 0
    return comfortable_difficulty


def calculate_comfortable_difficulties(difficulty_scores, difficulty_levels):
    """Calculate and return comfortable difficulty levels (in-order) based on the supplied scores."""
    comfortable_difficulty = None
    max_difficulty_low_score = None
    min_difficulty_high_score = None
    for difficulty_level, score in zip(difficulty_levels, difficulty_scores):
        if score is not None and score <= 0:
            max_difficulty_low_score = difficulty_level
    if max_difficulty_low_score is not None:
        comfortable_difficulty = max_difficulty_low_score
    if comfortable_difficulty is None:
        for difficulty_level, score in zip(reversed(difficulty_levels), reversed(difficulty_scores)):
            if score is not None and score > 0:
                min_difficulty_high_score = difficulty_level
        if min_difficulty_high_score is not None and min_difficulty_high_score - 1 >= difficulty_levels[0]:
            comfortable_difficulty = min_difficulty_high_score - 1
    if comfortable_difficulty is None:
        return difficulty_levels
    else:
        comfortable_difficulty_index = difficulty_levels.index(comfortable_difficulty)
        return [
            comfortable_difficulty,
            *reversed(difficulty_levels[:comfortable_difficulty_index]),
            *difficulty_levels[comfortable_difficulty_index + 1:],
        ]


def get_uncomfortable_difficulties(comfortable_difficulties, difficulty_levels):
    """Calculate and return uncomfortable difficulty levels (in-order), using the supplied comfortable difficulties."""
    comfortable_difficulty = comfortable_difficulties[0]
    if comfortable_difficulty + 1 <= max(difficulty_levels):
        comfortable_difficulty += 1
    comfortable_difficulty_index = difficulty_levels.index(comfortable_difficulty)
    return [
        comfortable_difficulty,
        *difficulty_levels[comfortable_difficulty_index + 1:],
        *reversed(difficulty_levels[:comfortable_difficulty_index]),
    ]


def get_uncomfortable_concepts_or_contexts(scores):
    """
    Return uncomfortable concept or context numbers.

    In order, the concepts/contexts either have not been done recently/before, or the user has struggled to answer
    questions with them.
    """
    uncomfortable_categories = calculate_uncomfortable_concepts_or_contexts(scores['numbers'], scores['month'])
    if len(uncomfortable_categories) <= 1:
        uncomfortable_categories = calculate_uncomfortable_concepts_or_contexts(scores['numbers'], scores['all'])
    return uncomfortable_categories


def calculate_uncomfortable_concepts_or_contexts(category_nums, category_scores):
    """Calculate and return an uncomfortable concepts or contexts based on the supplied scores."""
    uncomfortable_concepts_or_contexts = []
    excluded_category_nums = set()
    all_concepts_or_contexts_added = False
    while not all_concepts_or_contexts_added:
        categories_uncompleted = []
        highest_score_categories = []
        highest_score = -float('inf')
        for category_num, score in zip(category_nums, category_scores):
            if category_num not in excluded_category_nums:
                if score is None:
                    categories_uncompleted.append(category_num)
                elif len(highest_score_categories) < 1 or score == highest_score:
                    highest_score_categories.append(category_num)
                    highest_score = score
                elif score > highest_score:
                    highest_score_categories = [category_num]
                    highest_score = score
        if len(categories_uncompleted) > 0:
            uncomfortable_concepts_or_contexts.append(categories_uncompleted)
            excluded_category_nums.update(categories_uncompleted)
        elif len(highest_score_categories) > 0:
            uncomfortable_concepts_or_contexts.append(highest_score_categories)
            excluded_category_nums.update(highest_score_categories)
        else:
            all_concepts_or_contexts_added = True
    return uncomfortable_concepts_or_contexts
