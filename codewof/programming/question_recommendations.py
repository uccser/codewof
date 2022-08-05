"""Question recommendations for codeWOF."""

import statistics

from programming.models import DifficultyLevel, ProgrammingConcepts, QuestionContexts


def get_recommendation_values(info):
    """Get the recommendation values for the difficulty, concept, and context (unfinished)."""
    scores = get_scores(info)
    comfortable_difficulty = get_comfortable_difficulty(scores['difficulty'])
    uncomfortable_concepts = get_uncomfortable_concepts_or_contexts(scores['concept'])
    uncomfortable_contexts = get_uncomfortable_concepts_or_contexts(scores['context'])
    return comfortable_difficulty, uncomfortable_concepts, uncomfortable_contexts


def get_scores(info):
    """
    Return a dictionary of scores from the given tracked information.

    Creates scores based on all questions answered, and those answered within the past month.
    """
    difficulty_quantity = len(DifficultyLevel.objects.all())
    concept_quantity = len(ProgrammingConcepts.objects.all())
    context_quantity = len(QuestionContexts.objects.all())
    return {
        'difficulty': {
            'quantity': difficulty_quantity,
            'all': generate_scores(difficulty_quantity, info['all']['difficulty_level']),
            'month': generate_scores(difficulty_quantity, info['month']['difficulty_level']),
        },
        'concept': {
            'quantity': concept_quantity,
            'all': generate_scores(concept_quantity, info['all']['concept_num']),
            'month': generate_scores(concept_quantity, info['month']['concept_num']),
        },
        'context': {
            'quantity': context_quantity,
            'all': generate_scores(context_quantity, info['all']['context_num']),
            'month': generate_scores(context_quantity, info['month']['context_num']),
        },
    }


def generate_scores(quantity, info_category):
    """Generate and return the scores based on a given information category (e.g. difficulty)."""
    scores = [None] * quantity
    for category_num in range(quantity):
        if category_num in info_category:
            if scores[category_num] is None:
                scores[category_num] = 0
            scores[category_num] -= info_category[category_num]['num_solved']
            scores[category_num] += statistics.mean(info_category[category_num]['attempts']) - 1
    return scores


def get_comfortable_difficulty(scores):
    """Return a comfortable difficulty level (reasonable for the user to solve, not too hard or easy)."""
    difficulty_levels = list(range(scores['quantity']))
    difficulty_scores = scores['month']
    comfortable_difficulty = calculate_comfortable_difficulty(difficulty_levels, difficulty_scores)
    if comfortable_difficulty is None:
        difficulty_scores = scores['all']
        comfortable_difficulty = calculate_comfortable_difficulty(difficulty_levels, difficulty_scores)
    if comfortable_difficulty is None:
        comfortable_difficulty = None  # TODO: find new difficulty
    return comfortable_difficulty


def calculate_comfortable_difficulty(difficulty_levels, difficulty_scores):
    """Calculate and return a comfortable difficulty level based on the supplied scores."""
    if len(difficulty_levels) < 1:
        return None
    max_difficulty_low_score = None
    min_difficulty_high_score = None
    for difficulty_level, score in zip(difficulty_levels, difficulty_scores):
        if score is not None and score <= 0:
            max_difficulty_low_score = difficulty_level
    if max_difficulty_low_score is not None:
        return max_difficulty_low_score
    for difficulty_level, score in zip(reversed(difficulty_levels), reversed(difficulty_scores)):
        if score is not None and score > 0:
            min_difficulty_high_score = difficulty_level
    if min_difficulty_high_score is not None and min_difficulty_high_score - 1 >= difficulty_levels[0]:
        return min_difficulty_high_score - 1


def get_uncomfortable_concepts_or_contexts(scores):
    """
    Return an uncomfortable concept or context level.

    The concept or context either hasn't been done recently/before, or the user has struggled to answer questions with
    them.
    """
    category_nums = list(range(scores['quantity']))
    category_scores = scores['month']
    uncomfortable_categories = calculate_uncomfortable_concepts_or_contexts(category_nums, category_scores)
    if len(uncomfortable_categories) < 1:
        category_scores = scores['all']
        uncomfortable_categories = calculate_uncomfortable_concepts_or_contexts(category_nums, category_scores)
    if len(uncomfortable_categories) < 1:
        uncomfortable_categories = None  # TODO: find new concepts/contexts
    return uncomfortable_categories


def calculate_uncomfortable_concepts_or_contexts(category_nums, category_scores):
    """Calculate and return an uncomfortable concept or context based on the supplied scores."""
    if len(category_nums) < 1:
        return []
    categories_unattempted = []
    highest_score_categories = []
    highest_score = -float('inf')
    for category_num, score in zip(category_nums, category_scores):
        if score is None:
            categories_unattempted.append(category_num)
        elif len(highest_score_categories) < 1 or score == highest_score:
            highest_score_categories.append(category_num)
            highest_score = score
        elif score > highest_score:
            highest_score_categories = [category_num]
            highest_score = score
    if len(categories_unattempted) > 0:
        return categories_unattempted
    else:
        return highest_score_categories
