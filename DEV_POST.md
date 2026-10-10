# Prove It Outside

*Tags: #devchallenge #hf26challenge*

## What I Built

Prove It Outside is a small tool for testing AI predictions about the physical world. An open-weight model predicts which of two nearby places is quieter and states its confidence. I go to both places, record sound with my phone, and the tool scores the prediction with a Brier score. The tool also checks whether my measurements can separate the two places at all. If they can't, it refuses to score the models.

## Demo

[Add a short screen recording: enter predictions, lock them, measure location A and B, show the score or the inconclusive verdict.]

[Add a photo or clip of the field measurement.]

## Code

[Repo link]

Single-file `index.html`, no build step, no network calls. Full limitations are in `README.md`.

## How I Built It

- Vanilla HTML/JS. The Web Audio API (`AnalyserNode`) computes frame RMS in dBFS. Each run takes per-second means over 30 s and reports the median.
- Predictions are JSON pasted from the model's output. Predictions lock before measurement.
- Scoring: Brier score per model, `(confidence − correct)²`, plus a repeatability check. If the within-site spread is at least the between-site gap, the run is inconclusive.

- The demo voiceover was generated with ElevenLabs text-to-speech (`tts_demo.py`). It is a closed service used only for narration; the predictions come from open-weight models running locally.

## Why Open Innovation Matters

The open-weight models are the core of the project, not a decoration. Any open model can be asked the same question and its prediction can be checked against the same physical measurement. That makes the comparison reproducible: anyone can rerun the prediction with their own open model and go outside. I used `qwen3:4b` and `llama3.2:3b`, both run locally with Ollama, five samples each at temperature 0.7.

## How It Differs From Existing Work

Existing AI forecasting benchmarks such as ForecastBench score models on events that resolve in the future, and SciPredict scores models on outcomes of published experiments. As far as I could find, neither uses a measurement the builder takes personally in the field as ground truth. Most other Touch Grass entries generate outdoor quests; this one asks whether an open model's claim about a place survives a measurement. I did not find an existing project that does exactly this, but my search was limited and I can't rule one out.

## What I Found

**Places:** A is the street directly in front of my college. B is the entrance area of the metro station closest to my home. The models were given only those two one-line descriptions, with no other detail.

**Predictions (locked before measuring, see `predictions.json`):** both models picked A (the street) as quieter. `qwen3:4b` gave 0.79 confidence with 5/5 samples agreeing. `llama3.2:3b` gave 0.78 with 4/5 agreeing.

**An early finding:** the `llama3.2:3b` explanation says "the street is likely to be noisier than the metro station entrance" while its pick is A, the street, as the quieter place. Its reason contradicts its answer. Since both models picked the same place, this experiment cannot separate them on accuracy; it can only say whether the shared prediction was right.

[Fill in after the field run: measured medians, repeatability, and the verdict. Report an inconclusive result honestly.]

## Limitations

- Relative dBFS from one uncalibrated phone mic, not dB(A).
- Wind, traffic and time of day are not controlled.
- A single experiment cannot show that one model is better.

## My Agent Session (optional)

[Link or DevRelay session, if used.]
