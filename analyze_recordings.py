#!/usr/bin/env python3
"""Offline cross-check of index.html's recording mode (same method, needs ffmpeg).

Usage: python3 analyze_recordings.py --seg 15 --a street1.mp3 street2.mp3 --b mcd.mp3

Each file is cut into up to two segments of --seg seconds. A run's level is the
energy-averaged dBFS over its segment. Verdict rule: inconclusive when the largest
within-place spread is at least the gap between place medians.
"""
import argparse, json, math, statistics, struct, subprocess


def runs_for(path, seg_sec):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-t", str(2 * seg_sec), "-f", "f32le",
                          "-ac", "2", "-ar", "48000", "-"], capture_output=True, check=True).stdout
    vals = struct.unpack(f"<{len(raw) // 4}f", raw)
    per_ch = 48000 * 2
    out = []
    for seg in range(2):
        start, end = seg * seg_sec * per_ch, (seg + 1) * seg_sec * per_ch
        chunk = vals[start:end]
        if len(chunk) < seg_sec * per_ch:
            break
        energy = sum(v * v for v in chunk) / len(chunk)
        out.append(round(10 * math.log10(energy + 1e-24), 2))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seg", type=int, default=30)
    ap.add_argument("--a", nargs="+", required=True)
    ap.add_argument("--b", nargs="+", required=True)
    ap.add_argument("--predictions", default="predictions.json")
    args = ap.parse_args()
    A = [r for f in args.a for r in runs_for(f, args.seg)]
    B = [r for f in args.b for r in runs_for(f, args.seg)]
    mA, mB = statistics.median(A), statistics.median(B)
    gap = abs(mA - mB)
    repA, repB = (max(A) - min(A)) if len(A) > 1 else None, (max(B) - min(B)) if len(B) > 1 else None
    res = {"A_runs": A, "B_runs": B, "A_level": round(mA, 2), "B_level": round(mB, 2),
           "gap": round(gap, 2), "spread_A": repA, "spread_B": repB}
    if repA is None or repB is None:
        res["verdict"] = "not scored: need two runs at each place"
    elif gap == 0 or max(repA, repB) >= gap:
        res["verdict"] = "INCONCLUSIVE"
    else:
        truth = "A" if mA < mB else "B"
        res["verdict"] = f"{truth} is quieter"
        res["scores"] = []
        for p in json.load(open(args.predictions)):
            ok = 1 if p["quieter"] == truth else 0
            res["scores"].append({"model": p["model"], "pick": p["quieter"], "confidence": p["confidence"],
                                  "correct": bool(ok), "brier": round((p["confidence"] - ok) ** 2, 3)})
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
