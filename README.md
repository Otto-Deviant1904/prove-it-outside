# Prove It Outside

Make an AI model put a falsifiable prediction about the physical world on trial.
Predict which of two nearby places is quieter, go there, measure, and score the prediction.

## Run

Open `index.html` in Chrome or Edge (microphone access needs a secure context; `file://` works in Chrome). Allow microphone access when asked. If the page reports the microphone API is unavailable, serve it locally instead: `python3 -m http.server 8000`, then open `http://localhost:8000`.

Scoring needs at least 2 runs at each place (the repeatability check).

## Workflow

1. **Predict.** Enter two locations. Paste each open model's prediction as JSON: which place is quieter, its confidence (0.5–1), and its reason. Give every model the same description of both places. Click **Lock predictions** before you leave.
2. **Measure.** Stand at location A for 30 s, then B. Repeat each at least once. The tool logs a median level in dBFS per run. Keep the same phone, same settings, and same posture. Record conditions.
3. **Score.** The tool compares site medians, checks repeatability, and reports either an inconclusive verdict or each model's Brier score (lower is better). Export the run as JSON.

## Known limitations (state these in any write-up)

- Levels are **relative dBFS from one uncalibrated phone mic**, not dB(A). Only compare within one session on one device.
- Wind, traffic and time of day are not controlled. Conditions are logged, not corrected.
- One experiment is one data point. No model is declared better from a single run.
- The inconclusive rule is a simple heuristic: if the within-site spread is at least as large as the between-site gap, the run is not scored.

## Files

- `index.html`: the whole tool (no build step, no server, no network calls).
- `run_models.py`: asks local Ollama models the same prompt several times and prints predictions (majority pick, mean confidence, agreement rate) as JSON for `index.html`. Standard library only.
- `DEV_POST.md`: draft write-up for the Hacktoberfest challenge.
