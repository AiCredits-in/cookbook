import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_MODEL = "openai/gpt-4o-mini"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise SystemExit(f"Could not read {path}: {exc}") from exc


def numbered_lines(text: str) -> str:
    return "\n".join(f"{idx}: {line}" for idx, line in enumerate(text.splitlines(), start=1))


def parse_json_response(content: str | None) -> dict[str, Any]:
    if not content:
        raise ValueError("Model returned an empty response.")
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model did not return valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Expected the model response to be a JSON object.")
    return data


def match_resume_to_jd(client: OpenAI, resume_text: str, jd_text: str, model: str) -> dict[str, Any]:
    system_prompt = (
        "You are a careful technical recruiter. Return only valid JSON. "
        "Do not invent resume facts. Every strength must quote a specific resume line number as evidence."
    )
    user_prompt = f"""
Compare the resume to the job description.

Return this JSON shape:
{{
  "match_score": 0,
  "recommendation": "strong_match | possible_match | weak_match",
  "summary": "one short paragraph",
  "strengths": [
    {{"resume_line": 1, "evidence": "quoted resume line", "why_it_matters": "reason"}}
  ],
  "gaps": [
    {{"jd_requirement": "requirement", "resume_evidence": "missing or weak evidence", "risk": "reason"}}
  ],
  "interview_questions": ["question"]
}}

Scoring guidance:
- 85-100: strong overlap with direct evidence.
- 60-84: plausible match with some missing evidence.
- 0-59: weak evidence for important requirements.

Resume with line numbers:
{numbered_lines(resume_text)}

Job description:
{jd_text}
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a resume against a job description.")
    parser.add_argument("--resume", type=Path, default=Path("sample_resume.txt"))
    parser.add_argument("--jd", type=Path, default=Path("sample_jd.txt"))
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

    resume_text = read_text(args.resume)
    jd_text = read_text(args.jd)

    try:
        result = match_resume_to_jd(client, resume_text, jd_text, args.model)
    except Exception as exc:  # API errors and JSON errors should be visible in a small demo.
        print(f"Failed to match resume: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

