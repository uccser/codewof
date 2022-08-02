"""
Skill and level tracking for codeWOF.
"""

from programming.codewof_utils import filter_attempts_in_past_month
from programming.models import Attempt


def get_level_and_skill_info(profile):
    """
    Returns a dictionary of level and skill information from a given profile, taking solved plus all attempts and those
    within the past month.
    """
    all_attempts = Attempt.objects.filter(profile=profile)
    solved = all_attempts.filter(passed_tests=True)
    return {
        'all': get_level_and_skill_dict(solved, all_attempts),
        'month': get_level_and_skill_dict(
            filter_attempts_in_past_month(solved),
            filter_attempts_in_past_month(all_attempts),
        ),
    }


def get_level_and_skill_dict(solved, all_attempts):
    """Returns a dictionary of level and skill information from a given set of solved and all attempts."""
    solved_without_duplicates = remove_duplicate_question_slugs(solved)
    levels_and_skills = {'difficulty_level': dict(), 'concept_num': dict(), 'context_num': dict()}
    for solved_attempt in solved_without_duplicates:
        question = solved_attempt.question
        num_attempts = len(all_attempts.filter(question__slug=question.slug))

        if question.difficulty_level.level not in levels_and_skills['difficulty_level']:
            levels_and_skills['difficulty_level'][question.difficulty_level.level] = {'num_solved': 0, 'attempts': []}
        levels_and_skills['difficulty_level'][question.difficulty_level.level]['num_solved'] += 1
        levels_and_skills['difficulty_level'][question.difficulty_level.level]['attempts'].append(num_attempts)

        for concept_num in set(concept.number for concept in question.concepts.all()):
            if concept_num not in levels_and_skills['concept_num']:
                levels_and_skills['concept_num'][concept_num] = {'num_solved': 0, 'attempts': []}
            levels_and_skills['concept_num'][concept_num]['num_solved'] += 1
            levels_and_skills['concept_num'][concept_num]['attempts'].append(num_attempts)

        for context_num in set(context.number for context in question.contexts.all()):
            if context_num not in levels_and_skills['context_num']:
                levels_and_skills['context_num'][context_num] = {'num_solved': 0, 'attempts': []}
            levels_and_skills['context_num'][context_num]['num_solved'] += 1
            levels_and_skills['context_num'][context_num]['attempts'].append(num_attempts)
    return levels_and_skills


def remove_duplicate_question_slugs(attempts):
    """Removes attempts with question slugs of another attempt, from a given set of attempts."""
    attempts_without_duplicates = []
    question_slugs = set()
    for attempt in attempts:
        slug = attempt.question.slug
        if slug not in question_slugs:
            attempts_without_duplicates.append(attempt)
        question_slugs.add(slug)
    return attempts_without_duplicates
