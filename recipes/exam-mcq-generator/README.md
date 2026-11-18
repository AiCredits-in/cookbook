# Exam MCQ Generator + Evaluator

Python:
```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://api.aicredits.in/v1",
    api_key=os.environ["AICREDITS_API_KEY"],  # get one at https://aicredits.in/dashboard/keys
)

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",  # or anthropic/claude-3-5-haiku, google/gemini-2.0-flash, deepseek/deepseek-chat, etc.
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

## Problem Statement

Teachers often have source notes but need quick practice questions. This recipe generates multiple-choice questions as structured JSON, then evaluates a student's submitted answers against the generated answer key.

## What You'll Learn

- Rubric prompting for classroom-style question generation
- Batch generation with JSON mode
- Deterministic evaluation against an answer key

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set AICREDITS_API_KEY
python generate_mcqs.py --topic Photosynthesis --source sample_source.txt --count 5 --out generated_mcqs.json
python evaluate_answers.py --questions generated_mcqs.json --answers sample_answers.json
```

## Example Output

Generator:

```json
{
  "topic": "Photosynthesis",
  "questions": [
    {
      "id": "q1",
      "question": "What does chlorophyll capture during photosynthesis?",
      "options": {
        "A": "Oxygen",
        "B": "Light energy",
        "C": "Glucose",
        "D": "Soil minerals"
      },
      "correct_answer": "B",
      "explanation": "The source says chlorophyll captures light energy.",
      "source_evidence": "Chlorophyll in the leaves captures light energy."
    }
  ]
}
```

Evaluator:

```json
{
  "student_name": "Riya",
  "score": 4,
  "total": 5,
  "percentage": 80.0,
  "feedback": [
    {
      "id": "q1",
      "submitted_answer": "B",
      "correct_answer": "B",
      "is_correct": true,
      "feedback": "Correct."
    }
  ]
}
```

## Cost To Run This Demo

The generation step usually sends under 1,500 input tokens and receives around 800-1,200 output tokens for five questions. A reasonable demo estimate on a gpt-4o-mini-class model is ~₹0.10-₹0.75, while evaluation is local and free. Exact model prices change, so check https://aicredits.in/pricing before estimating real classroom usage.
