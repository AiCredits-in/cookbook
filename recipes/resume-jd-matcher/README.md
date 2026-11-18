# Resume JD Matcher

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

Given a resume and a job description, produce a 0-100 match score with evidence-backed strengths, gaps, and interview questions. The script asks the model to quote numbered resume lines so the recommendation is grounded in the supplied text.

## What You'll Learn

- JSON mode with `response_format={"type": "json_object"}`
- Prompt design that asks for evidence instead of broad claims
- Model IDs in `<provider>/<model-name>` format through one AICredits endpoint

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set AICREDITS_API_KEY
python match_resume.py --resume sample_resume.txt --jd sample_jd.txt
```

Optional model override:

```bash
python match_resume.py --model anthropic/claude-3-5-haiku
```

## Example Output

```json
{
  "match_score": 86,
  "recommendation": "strong_match",
  "summary": "The resume has direct evidence for Python services, retrieval, PostgreSQL, Docker, and helpdesk workflows.",
  "strengths": [
    {
      "resume_line": 5,
      "evidence": "Built a FastAPI service that processed 20,000 support tickets per month.",
      "why_it_matters": "Matches Python service and support workflow requirements."
    }
  ],
  "gaps": [
    {
      "jd_requirement": "Structured JSON outputs",
      "resume_evidence": "No explicit resume line mentions JSON schema design.",
      "risk": "Ask in interview before assuming production experience."
    }
  ],
  "interview_questions": [
    "How did you evaluate retrieved document snippets in the helpdesk bot?"
  ]
}
```

## Cost To Run This Demo

For the included sample files, expect roughly 1,500-2,500 input tokens and a few hundred output tokens. A reasonable demo estimate on a gpt-4o-mini-class model is ~₹0.10-₹0.50, but exact prices change. Check https://aicredits.in/pricing before estimating real usage.
