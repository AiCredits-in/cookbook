# Model Eval Harness

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

The best model for your task may not be the most famous one. This harness runs the same prompt across multiple AICredits model IDs and compares latency, token usage, output length, and an approximate relative cost.

## What You'll Learn

- Building a simple eval loop
- Reading `response.usage` token counts
- Comparing cost and quality tradeoffs across providers

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set AICREDITS_API_KEY
python evaluate_models.py
```

Custom prompt and model list:

```bash
python evaluate_models.py \
  --prompt "Summarize this refund policy for a confused customer." \
  --models openai/gpt-4o-mini deepseek/deepseek-chat google/gemini-2.0-flash
```

## Example Output

```text
model                       latency_s  prompt  completion  total  approx_cost  output_chars  status
--------------------------  ---------  ------  ----------  -----  -----------  ------------  ------
openai/gpt-4o-mini          1.12       34      118         152    ₹0.0063      612           ok
deepseek/deepseek-chat      1.45       34      126         160    ₹0.0128      688           ok
google/gemini-2.0-flash     0.94       34      101         135    ₹0.0044      540           ok

Summary
- Fastest: google/gemini-2.0-flash (0.94s)
- Cheapest by approximate table: google/gemini-2.0-flash (₹0.0044)
- Longest output: deepseek/deepseek-chat (688 chars)
```

## Cost To Run This Demo

This harness makes one request per model. With four short responses, a reasonable demo estimate is ~₹0.25-₹1.50 across the default model list, depending on output length and provider pricing. The hardcoded table in `evaluate_models.py` is only for relative comparison; check https://aicredits.in/pricing for exact current prices.
