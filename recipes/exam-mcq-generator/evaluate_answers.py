import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"Could not read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{path} must contain a JSON object.")
    return data


def evaluate_answers(question_set: dict[str, Any], submission: dict[str, Any]) -> dict[str, Any]:
    questions = question_set.get("questions")
    answers = submission.get("answers")
    if not isinstance(questions, list) or not questions:
        raise ValueError("Question file must contain a non-empty questions list.")
    if not isinstance(answers, dict):
        raise ValueError("Answers file must contain an answers object.")

    feedback = []
    correct_count = 0

    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("Each question must be a JSON object.")
        question_id = str(question.get("id", ""))
        correct_answer = str(question.get("correct_answer", "")).upper()
        submitted_answer = str(answers.get(question_id, "")).upper()
        is_correct = submitted_answer == correct_answer
        if is_correct:
            correct_count += 1
        feedback.append(
            {
                "id": question_id,
                "question": question.get("question", ""),
                "submitted_answer": submitted_answer or None,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "feedback": "Correct." if is_correct else question.get("explanation", "Review the source text."),
            }
        )

    total = len(questions)
    return {
        "student_name": submission.get("student_name", "Unknown student"),
        "score": correct_count,
        "total": total,
        "percentage": round((correct_count / total) * 100, 2),
        "feedback": feedback,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate submitted MCQ answers.")
    parser.add_argument("--questions", type=Path, default=Path("generated_mcqs.json"))
    parser.add_argument("--answers", type=Path, default=Path("sample_answers.json"))
    args = parser.parse_args()

    try:
        question_set = load_json(args.questions)
        submission = load_json(args.answers)
        result = evaluate_answers(question_set, submission)
    except Exception as exc:
        print(f"Failed to evaluate answers: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

