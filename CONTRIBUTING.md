# Contributing to the AICredits Cookbook

Thanks for helping. Good recipes help other developers get started quickly.

## Safety first

This repository is public.

- **Never commit a real API key.** Keys belong in a local `.env`, which is git-ignored. Only `.env.example` with a placeholder is committed.
- **Never commit private data** in sample files. Use made-up or public-domain samples.
- If you committed a key by mistake, revoke it in your AICredits dashboard first, then remove it from your branch.

## Ways to contribute

- **Fix a bug or typo in a recipe:** open a pull request, or use the [recipe bug form](../../issues/new?template=recipe_bug.yml).
- **Propose a new recipe:** use the [recipe proposal form](../../issues/new?template=recipe_request.yml) before you start. We will confirm it fits.
- **Pick up an idea:** [PROJECT_IDEAS.md](PROJECT_IDEAS.md) lists ideas that nobody has built yet. Comment on an issue or open one to claim it.
- **Questions:** use [community discussions](https://github.com/AiCredits-in/community/discussions).

## What a good recipe looks like

Each recipe lives in `recipes/<recipe-name>/` and is a standalone project.

| File | Purpose |
|---|---|
| `README.md` | What it does, what you learn, setup, run command, and a cost note. |
| `requirements.txt` | Pinned or minimum versions of the few dependencies it needs. |
| `.env.example` | `AICREDITS_API_KEY=sk-...` and any other variables, with placeholders only. |
| Source file(s) | Small, readable, with comments where the idea is not obvious. |
| Sample data | Small made-up or public-domain inputs so people can run it immediately. |

Guidelines:

- **Small and runnable.** Someone should get a result within a few minutes of cloning.
- **Beginner-friendly.** Minimal dependencies, clear names, no clever tricks.
- **One endpoint.** Use the OpenAI-compatible endpoint `https://api.aicredits.in/v1` with an OpenAI SDK, and model IDs in `<provider>/<model-name>` format.
- **Honest costs.** Give a rough cost range in INR and point readers to <https://aicredits.in/pricing> for current prices. Do not hardcode price tables.
- **Read keys from the environment.** Use `AICREDITS_API_KEY`. Never hardcode a key.
- **Tested before you open the PR.** Run the recipe end to end with your own key.

## Pull requests

1. For anything bigger than a typo, open an issue first.
2. Fork the repo and branch from `main`.
3. Keep each pull request to one recipe or one fix.
4. Fill in the pull request template.
5. A maintainer reviews every pull request. We squash-merge.

## License

By contributing you agree that your contribution is licensed under the [MIT License](LICENSE).
