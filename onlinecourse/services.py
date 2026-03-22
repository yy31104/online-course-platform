from typing import Dict, List

from .models import Question


def extract_selected_choice_ids(post_data) -> List[int]:
    selected_choice_ids = []
    for key, value in post_data.items():
        if not key.startswith("choice"):
            continue
        try:
            selected_choice_ids.append(int(value))
        except (TypeError, ValueError):
            continue
    return selected_choice_ids


def calculate_submission_result(course, submission) -> Dict:
    selected_choice_ids = list(submission.choices.values_list("id", flat=True))
    questions = Question.objects.filter(course=course).prefetch_related("choice_set")

    total_score = 0
    total_possible = 0
    question_results = []
    for question in questions:
        score = question.is_get_score(selected_choice_ids)
        total_score += score
        total_possible += question.grade
        question_results.append(
            {
                "question": question,
                "choices": question.choice_set.all(),
                "score": score,
            }
        )

    grade = int((total_score / total_possible) * 100) if total_possible else 0
    return {
        "grade": grade,
        "total_score": total_score,
        "total_possible": total_possible,
        "selected_choice_ids": selected_choice_ids,
        "question_results": question_results,
    }
