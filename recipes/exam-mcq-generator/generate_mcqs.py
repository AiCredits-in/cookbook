import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_MODEL = "openai/gpt-4o-mini"


def read_source(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise SystemExit(f"Could not read {path}: {exc}") from exc


def parse_json_response(content: str | None) -> dict[str, Any]:
    if not content:
        raise ValueError("Model returned an empty response.")
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model did not return valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object.")
    return data


def generate_mcqs(client: OpenAI, topic: str, source_text: str, count: int, model: str) -> dict[str, Any]:
    if count < 1:
        raise ValueError("Question count must be at least 1.")

    system_prompt = (
        "You are a careful teacher creating exam questions from source material. "
        "Return only valid JSON. Keep every correct answer supported by the source text."
    )
    user_prompt = f"""
Create {count} multiple-choice questions for the topic: {topic}

Return this JSON shape:
{{
  "topic": "{topic}",
  "questions": [
    {{
      "id": "q1",
      "question": "question text",
      "options": {{"A": "option", "B": "option", "C": "option", "D": "option"}},
      "correct_answer": "A",
      "explanation": "why the answer is correct",
      "source_evidence": "short quote or paraphrase from the source"
    }}
  ]
}}

Rules:
- Use IDs q1 through q{count}.
- Each question must have exactly four options: A, B, C, and D.
- The correct answer must be one of A, B, C, or D.
- Avoid trick questions unless the source text clearly supports them.

Source text:
{source_text}
""".strip()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )
    return parse_json_response(response.choices[0].message.content)


def validate_question_set(data: dict[str, Any]) -> None:
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("Response JSON must include a non-empty questions list.")
    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("Each question must be a JSON object.")
        options = question.get("options")
        if not isinstance(options, dict) or set(options.keys()) != {"A", "B", "C", "D"}:
            raise ValueError(f"Question {question.get('id', '<unknown>')} must include options A-D.")
        if question.get("correct_answer") not in {"A", "B", "C", "D"}:
            raise ValueError(f"Question {question.get('id', '<unknown>')} has an invalid correct_answer.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate MCQs from source text.")
    parser.add_argument("--topic", default="Photosynthesis")
    parser.add_argument("--source", type=Path, default=Path("sample_source.txt"))
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--out", type=Path, default=Path("generated_mcqs.json"))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("AICREDITS_API_KEY")
    if not api_key:
        print("Missing AICREDITS_API_KEY. Copy .env.example to .env and add your key.", file=sys.stderr)
        return 2

    client = OpenAI(
        base_url="https://api.aicredits.in/v1",
        api_key=api_key,
    )

    source_text = read_source(args.source)
    try:
        question_set = generate_mcqs(client, args.topic, source_text, args.count, args.model)
        validate_question_set(question_set)
    except Exception as exc:
        print(f"Failed to generate MCQs: {exc}", file=sys.stderr)
        return 1

    args.out.write_text(json.dumps(question_set, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(question_set['questions'])} questions to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

