"""
Question recommendations for codeWOF.
"""

import statistics

from programming.models import DifficultyLevel, ProgrammingConcepts, QuestionContexts


def get_recommendation_values(info):
    """Gets the recommendation values for the difficulty, concept, and context (unfinished)."""
    difficulty_quantity = len(DifficultyLevel.objects.all())
    concept_quantity = len(ProgrammingConcepts.objects.all())
    context_quantity = len(QuestionContexts.objects.all())
    scores = get_scores(info, difficulty_quantity, concept_quantity, context_quantity)
    comfortable_difficulty = get_comfortable_difficulty(scores, list(range(difficulty_quantity)))
    return comfortable_difficulty


def get_scores(info, difficulty_quantity, concept_quantity, context_quantity):
    """
    Returns a dictionary of scores from the given tracked information, with scores based on all questions answered, and
    those answered within the past month.
    """
    return {
        'all': {
            'difficulty': generate_scores(difficulty_quantity, info['all']['difficulty_level']),
            'concept': generate_scores(concept_quantity, info['all']['concept_num']),
            'context': generate_scores(context_quantity, info['all']['context_num']),
        },
        'month': {
            'difficulty': generate_scores(difficulty_quantity, info['month']['difficulty_level']),
            'concept': generate_scores(concept_quantity, info['month']['concept_num']),
            'context': generate_scores(context_quantity, info['month']['context_num']),
        },
    }


def generate_scores(quantity, info_category):
    """Generates and returns the scores based on a given information category (e.g. difficulty)."""
    scores = [None] * quantity
    for category_num in range(quantity):
        if category_num in info_category:
            if scores[category_num] is None:
                scores[category_num] = 0
            scores[category_num] -= info_category[category_num]['num_solved']
            scores[category_num] += statistics.mean(info_category[category_num]['attempts']) - 1
    return scores


def get_comfortable_difficulty(scores, difficulty_levels):
    """Returns a comfortable difficulty level (reasonable for the user to solve, not too hard or easy)."""
    difficulty_scores = scores['month']['difficulty']
    comfortable_difficulty = calculate_comfortable_difficulty(difficulty_scores, difficulty_levels)
    if comfortable_difficulty is None:
        difficulty_scores = scores['all']['difficulty']
        comfortable_difficulty = calculate_comfortable_difficulty(difficulty_scores, difficulty_levels)
    if comfortable_difficulty is None:
        comfortable_difficulty = None
    return comfortable_difficulty


def calculate_comfortable_difficulty(difficulty_scores, difficulty_levels):
    """Calculates and returns a comfortable difficulty level based on the supplied scores."""
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
