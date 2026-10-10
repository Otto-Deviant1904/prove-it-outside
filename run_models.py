#!/usr/bin/env python3
"""Ask local Ollama models the same question and print predictions as JSON.

Usage:
  python3 run_models.py --models qwen3:4b llama3.2:3b \
      --desc-a "Residential side street..." --desc-b "Main road bus stop..." \
      --when "Sunday 4 PM, dry" --samples 5

Output is a JSON array to paste into index.html. Per model: the majority-vote
pick, the mean stated confidence among the samples that agree with the vote,
and the agreement rate across samples.
"""
import argparse, json, statistics, sys, urllib.error, urllib.request

URL = "http://localhost:11434/api/generate"


def build_prompt(a, b, when):
    return (
        "Two places will be compared with a phone microphone.\n"
        f"Place A: {a.strip()}\nPlace B: {b.strip()}\n"
        f"Conditions: {when.strip() or 'unspecified'}\n\n"
        "Which place will have the lower average sound level over a 30-second measurement?\n"
        'Answer with JSON only: {"quieter":"A" or "B","confidence":<number from 0.5 to 1, '
        'your probability that your pick is correct>,"reason":"<one sentence>"}'
    )


def ask(model, prompt, temperature):
    body = json.dumps({
        "model": model, "prompt": prompt, "stream": False, "format": "json",
        "options": {"temperature": temperature},
    }).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())["response"]
    except urllib.error.HTTPError as e:
        sys.exit(f"Ollama HTTP {e.code} for model {model!r} (installed? try: ollama pull {model})")
    except urllib.error.URLError as e:
        sys.exit(f"Cannot reach Ollama at {URL}: {e.reason} (start it with: ollama serve)")


def parse(text):
    try:
        d = json.loads(text)
        q = str(d.get("quieter", "")).strip().upper()
        c = float(d.get("confidence"))
        if q in ("A", "B") and 0.5 <= c <= 1:
            return q, c, str(d.get("reason", ""))
    except (ValueError, TypeError, json.JSONDecodeError):
        pass
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--models", nargs="+", required=True)
    p.add_argument("--desc-a", required=True)
    p.add_argument("--desc-b", required=True)
    p.add_argument("--when", default="")
    p.add_argument("--samples", type=int, default=5)
    p.add_argument("--temperature", type=float, default=0.7)
    args = p.parse_args()

    prompt = build_prompt(args.desc_a, args.desc_b, args.when)
    out = []
    for model in args.models:
        good = []
        for _ in range(args.samples):
            r = parse(ask(model, prompt, args.temperature))
            if r:
                good.append(r)
        if not good:
            out.append({"model": model, "error": "no valid answers"})
            continue
        votes = [g[0] for g in good]
        pick = max("AB", key=votes.count)
        agree = [g for g in good if g[0] == pick]
        out.append({
            "model": model,
            "quieter": pick,
            "confidence": round(statistics.mean(g[1] for g in agree), 2),
            "agreement": round(len(agree) / len(good), 2),
            "valid_samples": len(good),
            "reason": agree[0][2],
        })
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
