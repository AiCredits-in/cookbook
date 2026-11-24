# AICredits Cookbook

Runnable example projects for students and new AI engineers building with an OpenAI-compatible LLM gateway in India.

AICredits is an LLM Gateway & Credit System at https://aicredits.in. It sits between your app and providers such as OpenAI, Anthropic, Google Gemini, DeepSeek, Mistral, xAI, and 300+ total models. You call one OpenAI-compatible API endpoint, prepaid credits are bought in INR via UPI/Razorpay, and wallet credits are FIFO-consumed with 1 year validity. No international credit card is needed.

## Why This Exists

Most AI tutorials assume you can create several provider accounts, add international payment cards, and manage billing separately. This cookbook keeps the examples simple: one API key, one OpenAI-compatible client, and model IDs in `<provider>/<model-name>` format.

## Get An API Key

1. Create or open your AICredits account at https://aicredits.in.
2. Add credits to your wallet.
3. Create an API key at https://aicredits.in/dashboard/keys.
4. Put it in each recipe's `.env` file as:

```bash
AICREDITS_API_KEY=sk-...
```

Read the full docs at https://aicredits.in/docs.

## Run A Recipe

Each recipe is a standalone Python 3.10+ project:

```bash
cd recipes/resume-jd-matcher
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and add your AICREDITS_API_KEY
python match_resume.py --resume sample_resume.txt --jd sample_jd.txt
```

Current full recipes:

- [Resume JD Matcher](recipes/resume-jd-matcher/README.md)
- [Exam MCQ Generator](recipes/exam-mcq-generator/README.md)
- [Model Eval Harness](recipes/model-eval-harness/README.md)

More ideas are listed in [PROJECT_IDEAS.md](PROJECT_IDEAS.md).

## Contributing

Contributions are welcome. Keep examples small, runnable, and beginner-friendly. Prefer minimal dependencies, real sample data, clear setup steps, and honest cost notes that point readers to https://aicredits.in/pricing for current prices.

- Read [CONTRIBUTING.md](CONTRIBUTING.md) for what a good recipe looks like.
- Found a problem with a recipe? [Open a recipe bug](../../issues/new?template=recipe_bug.yml).
- Have an idea? [Propose a recipe](../../issues/new?template=recipe_request.yml).
- Questions: [community discussions](https://github.com/AiCredits-in/community/discussions).

**This repository is public. Never commit a real API key.** Keep keys in a local `.env` file, which is git-ignored.

