"""Question recommendations for codeWOF."""

import random
import statistics

from programming.models import DifficultyLevel, ProgrammingConcepts, QuestionContexts, Attempt, Question
from programming.skill_and_level_tracking import get_level_and_skill_info


difficulty_levels = sorted(list(set([difficulty.level for difficulty in DifficultyLevel.objects.all()])))
concept_numbers = sorted(list(set([concept.number for concept in ProgrammingConcepts.objects.all()])))
context_numbers = sorted(list(set([context.number for context in QuestionContexts.objects.all()])))


def get_recommended_questions(profile):
    """Get the recommended questions based on the user's previously answered questions."""
    level_and_skill_info = get_level_and_skill_info(profile)
    scores = get_scores(level_and_skill_info)
    recommended_questions = calculate_recommended_questions(profile, scores)
    return recommended_questions


def calculate_recommended_questions(profile, scores):
    """
    Get the recommended questions from calculations based on the provided scores and user.

    Retrieves the recommendation values for the difficulty, concept, and context, and uses this to calculate the
    recommended questions.
    """
    comfortable_difficulties = get_comfortable_difficulties(scores['difficulty'])
    uncomfortable_concepts = get_uncomfortable_concepts_or_contexts(scores['concept'], concept_numbers)
    uncomfortable_contexts = get_uncomfortable_concepts_or_contexts(scores['context'], context_numbers)
    comfortable_difficulty_recommendations = get_comfortable_difficulty_recommendations(
        profile, comfortable_difficulties, uncomfortable_concepts, uncomfortable_contexts
    )
    recommended_questions = []
    if len(comfortable_difficulty_recommendations) > 0:
        recommended_questions.append(random.choice(comfortable_difficulty_recommendations))
    return recommended_questions


def get_comfortable_difficulty_recommendations(
    profile, comfortable_difficulties, uncomfortable_concepts, uncomfortable_contexts
):
    """
    Get the comfortable difficulty, uncomfortable concepts/contexts, question recommendations.

    Iterates through possible combinations to find a valid question that matches the criteria.
    """
    solved_question_slugs = get_solved_question_slugs(profile)

    questions = Question.objects.distinct('pk').select_subclasses()
    initial_concepts = uncomfortable_concepts[0]
    for difficulty in comfortable_difficulties:
        comfortable_difficulty_questions = questions.filter(difficulty_level__level=difficulty)
        for contexts in uncomfortable_contexts:
            comfortable_difficulty_recommendations = calculate_comfortable_difficulty_questions(
                solved_question_slugs, comfortable_difficulty_questions, initial_concepts, contexts
            )
            if len(comfortable_difficulty_recommendations) > 0:
                return comfortable_difficulty_recommendations
        for concepts in uncomfortable_concepts:
            comfortable_difficulty_recommendations = calculate_comfortable_difficulty_questions(
                solved_question_slugs, comfortable_difficulty_questions, concepts
            )
            if len(comfortable_difficulty_recommendations) > 0:
                return comfortable_difficulty_recommendations
        comfortable_difficulty_recommendations = calculate_comfortable_difficulty_questions(
            solved_question_slugs, comfortable_difficulty_questions
        )
        if len(comfortable_difficulty_recommendations) > 0:
            return comfortable_difficulty_recommendations
    return []


def get_solved_question_slugs(profile):
    """Get the question slugs of those solved by the user."""
    solved_question_slugs = set()
    solved_attempts = Attempt.objects.filter(profile=profile, passed_tests=True).all()
    for solved_attempt in solved_attempts:
        solved_question_slugs.add(solved_attempt.question.slug)
    return solved_question_slugs


def calculate_comfortable_difficulty_questions(passed_question_slugs, questions, concepts=None, contexts=None):
    """Calculate and return the comfortable difficulty, uncomfortable concepts/contexts, question recommendations."""
    comfortable_difficulty_questions = []
    for question in questions:
        if question.slug not in passed_question_slugs:
            filters = []
            if concepts is not None:
                question_concepts = [concept.number for concept in question.concepts.all()]
                filters.append(
                    any(uncomfortable_concept in question_concepts for uncomfortable_concept in concepts))
            if contexts is not None:
                question_contexts = [context.number for context in question.contexts.all()]
                filters.append(
                    any(uncomfortable_context in question_contexts for uncomfortable_context in contexts))
            if all(filters):
                comfortable_difficulty_questions.append(question)
    return comfortable_difficulty_questions


def get_scores(level_and_skill_info):
    """
    Return a dictionary of scores from the given tracked information.

    Creates scores based on all questions answered, and those answered within the past month.
    """
    return {
        'difficulty': {
            'all': generate_scores(difficulty_levels, level_and_skill_info['all']['difficulty_level']),
            'month': generate_scores(difficulty_levels, level_and_skill_info['month']['difficulty_level']),
        },
        'concept': {
            'all': generate_scores(concept_numbers, level_and_skill_info['all']['concept_num']),
            'month': generate_scores(concept_numbers, level_and_skill_info['month']['concept_num']),
        },
        'context': {
            'all': generate_scores(context_numbers, level_and_skill_info['all']['context_num']),
            'month': generate_scores(context_numbers, level_and_skill_info['month']['context_num']),
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


def get_comfortable_difficulties(scores):
    """Return comfortable difficulty levels (reasonable for the user to solve, not too hard or easy, in-order)."""
    comfortable_difficulty = calculate_comfortable_difficulties(scores['month'])
    if comfortable_difficulty is None:
        comfortable_difficulty = calculate_comfortable_difficulties(scores['all'])
    if comfortable_difficulty is None:
        comfortable_difficulty = 0
    return comfortable_difficulty


def calculate_comfortable_difficulties(difficulty_scores):
    """Calculate and return a comfortable difficulty levels (in-order) based on the supplied scores."""
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


def get_uncomfortable_concepts_or_contexts(scores, category_nums):
    """
    Return uncomfortable concept or context numbers.

    In order, the concepts/contexts either have not been done recently/before, or the user has struggled to answer
    questions with them.
    """
    uncomfortable_categories = calculate_uncomfortable_concepts_or_contexts(category_nums, scores['month'])
    if len(uncomfortable_categories) <= 1:
        uncomfortable_categories = calculate_uncomfortable_concepts_or_contexts(category_nums, scores['all'])
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
