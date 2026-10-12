# Prove It Outside

Make an AI model put a falsifiable prediction about the physical world on trial.
Predict which of two nearby places is quieter, go there, measure, and score the prediction.

## Run

On a phone, open the https GitHub Pages link: https://otto-deviant1904.github.io/prove-it-outside/ (microphone access needs a secure context; a local network address will not work). On a laptop, open `index.html` in Chrome or Edge via `file://`, or run `python3 -m http.server 8000` and open `http://localhost:8000`. Allow microphone access when asked. Keep the screen on and the page visible while measuring; short or silent runs are discarded.

Scoring needs at least 2 runs at each place (the repeatability check).

## Workflow

1. **Predict.** Enter two locations. For each open model, enter which place it says is quieter and its confidence in percent (or paste the JSON that `run_models.py` prints). Give every model the same description of both places. Click **Lock predictions** before you leave.
2. **Measure.** Stand at location A for 30 s and repeat once, then do the same at B (if the places are far apart, do both runs at one place back to back and note the times). The tool logs an energy-averaged level in dBFS per run. Keep the same phone, same settings, and same posture. Record conditions.
3. **Score.** The tool compares site medians, checks repeatability, and reports either an inconclusive verdict or each model's Brier score (lower is better). Export the run as JSON.

## Recording mode (no microphone)

Under step 3, "Analyze a recording instead" takes an audio file per place (at least 30 s). Each full 30 s segment (up to two per file) becomes a run. You must enter where the recording is from (title, author, license, link). That source is saved with the results and printed in the score, which says "RECORDED AUDIO FILES, not live measurements". Levels from different recordings are only comparable if similar equipment and settings were used.

## Known limitations (state these in any write-up)

- Levels are energy-averaged **relative dBFS from one uncalibrated phone mic**, not dB(A). Only compare within one session on one device.
- Wind, traffic and time of day are not controlled. Conditions are logged, not corrected. The score output prints the time between the A runs and the B runs, because a large gap makes time of day a confound.
- One experiment is one data point. No model is declared better from a single run.
- The inconclusive rule is a simple heuristic: if the within-site spread is at least as large as the between-site gap, the run is not scored.

## Files

- `index.html`: the whole tool (no build step, no server, no network calls).
- `run_models.py`: asks local Ollama models the same prompt several times and prints predictions (majority pick, confidence over all samples, agreement rate, raw samples) as JSON for `index.html`. Standard library only.
- `DEV_POST.md`: draft write-up for the Hacktoberfest challenge.
