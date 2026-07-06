import argparse
import os
import sys
import time
from dataclasses import dataclass
from typing import Iterable

from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_MODELS = [
    "openai/gpt-4o-mini",
    "anthropic/claude-3-5-haiku",
    "deepseek/deepseek-chat",
    "google/gemini-2.0-flash",
]

# Demo-only approximate INR per 1M tokens. Check https://aicredits.in/pricing for real prices.
APPROX_PRICING_INR_PER_1M = {
    "openai/gpt-4o-mini": {"input": 13.0, "output": 50.0},
    "anthropic/claude-3-5-haiku": {"input": 70.0, "output": 330.0},
    "deepseek/deepseek-chat": {"input": 25.0, "output": 95.0},
    "google/gemini-2.0-flash": {"input": 10.0, "output": 40.0},
}


@dataclass
class ModelResult:
    model: str
    latency_seconds: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    approx_cost_inr: float | None
    output: str
    error: str | None = None


def estimate_cost_inr(model: str, prompt_tokens: int | None, completion_tokens: int | None) -> float | None:
    pricing = APPROX_PRICING_INR_PER_1M.get(model)
    if pricing is None or prompt_tokens is None or completion_tokens is None:
        return None
    input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
    output_cost = (completion_tokens / 1_000_000) * pricing["output"]
    return input_cost + output_cost


def run_model(client: OpenAI, model: str, prompt: str) -> ModelResult:
    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are concise and practical. Answer the user's task directly.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        latency = time.perf_counter() - start
        usage = response.usage
        prompt_tokens = getattr(usage, "prompt_tokens", None) if usage else None
        completion_tokens = getattr(usage, "completion_tokens", None) if usage else None
        total_tokens = getattr(usage, "total_tokens", None) if usage else None
        output = response.choices[0].message.content or ""
        return ModelResult(
            model=model,
            latency_seconds=latency,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            approx_cost_inr=estimate_cost_inr(model, prompt_tokens, completion_tokens),
            output=output.strip(),
        )
    except Exception as exc:
        latency = time.perf_counter() - start
        return ModelResult(
            model=model,
            latency_seconds=latency,
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            approx_cost_inr=None,
            output="",
            error=str(exc),
        )


def format_money(value: float | None) -> str:
    return "n/a" if value is None else f"₹{value:.4f}"


def format_int(value: int | None) -> str:
    return "n/a" if value is None else str(value)


def table_rows(results: Iterable[ModelResult]) -> list[list[str]]:
    rows = [["model", "latency_s", "prompt", "completion", "total", "approx_cost", "output_chars", "status"]]
    for result in results:
        rows.append(
            [
                result.model,
                f"{result.latency_seconds:.2f}",
                format_int(result.prompt_tokens),
                format_int(result.completion_tokens),
                format_int(result.total_tokens),
                format_money(result.approx_cost_inr),
                str(len(result.output)),
                "error" if result.error else "ok",
            ]
        )
    return rows


def print_table(rows: list[list[str]]) -> None:
    widths = [max(len(row[col]) for row in rows) for col in range(len(rows[0]))]
    for index, row in enumerate(rows):
        line = "  ".join(cell.ljust(widths[col]) for col, cell in enumerate(row))
        print(line)
        if index == 0:
            print("  ".join("-" * width for width in widths))


def print_winners(results: list[ModelResult]) -> None:
    successful = [result for result in results if result.error is None]
    if not successful:
        print("\nNo successful model responses.")
        return

    fastest = min(successful, key=lambda result: result.latency_seconds)
    priced = [result for result in successful if result.approx_cost_inr is not None]
    cheapest = min(priced, key=lambda result: result.approx_cost_inr) if priced else None
    longest = max(successful, key=lambda result: len(result.output))

    print("\nSummary")
    print(f"- Fastest: {fastest.model} ({fastest.latency_seconds:.2f}s)")
    if cheapest:
        print(f"- Cheapest by approximate table: {cheapest.model} ({format_money(cheapest.approx_cost_inr)})")
    else:
        print("- Cheapest by approximate table: n/a")
    print(f"- Longest output: {longest.model} ({len(longest.output)} chars)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare one prompt across multiple AICredits models.")
    parser.add_argument(
        "--prompt",
        default="Explain photosynthesis to a class 8 student in five bullet points.",
    )
    parser.add_argument(
        "--models",
        nargs="*",
        default=DEFAULT_MODELS,
        help="Model IDs in provider/model-name format.",
    )
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

    results = [run_model(client, model, args.prompt) for model in args.models]
    print_table(table_rows(results))
    print_winners(results)

    for result in results:
        if result.error:
            print(f"\n{result.model} error:\n{result.error}")
        else:
            print(f"\n{result.model} output:\n{result.output}")

    return 0 if any(result.error is None for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

