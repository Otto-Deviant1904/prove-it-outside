# Prove It Outside: can an open model's guess survive a microphone?

*Tags: #devchallenge #hf26challenge*

## What I Built

AI models are happy to tell you things about places they have never been. The only way to check one of those claims is to go there. So I built a tool that makes the check the whole point.

Prove It Outside makes an open-weight model commit to a falsifiable prediction about the physical world: *which of two places will be quieter?* The prediction and the model's confidence are locked first. Then I walk to both places, record sound with my phone, and the tool scores each model with a Brier score. If my measurements are too noisy to tell the two places apart, the tool says **inconclusive** and refuses to score anyone.

The two places: Main Street in the city, in front of my college (A), and a convenience shop near a metro station (B), measured on a Sunday at 3 PM. The models were told only those one-line descriptions.

## Demo

[Demo video: prompt, locked predictions, four phone measurements, the score or inconclusive verdict.]

## Code

https://github.com/Otto-Deviant1904/prove-it-outside

- `index.html`: the whole tool, one file, no build step, no network calls.
- `run_models.py`: asks local Ollama models the same prompt several times and prints predictions.
- `predictions.json` and `predictions_command.txt`: the exact predictions and the command that produced them. They were committed in git at `e58013c` before any measurement.

## How I Built It

- **Models:** `qwen3:4b` and `llama3.2:3b`, both open-weight, run locally with Ollama. Each got the same one-line description of each place, seven samples at temperature 0.7. A model's pick is its majority vote; its confidence is the mean implied probability that the pick is right across all samples, so dissenting samples pull it down.
- **Measurement:** the Web Audio API reads the phone microphone for 30 seconds with echo cancellation, noise suppression and auto-gain switched off. The level of a run is the energy-averaged level in dBFS, which matches the question the models were asked ("lower average sound level"). Runs shorter than 27 seconds or with silent audio are discarded.
- **Scoring:** each place is measured at least twice. If the spread between runs at one place is as large as the gap between the two places, the verdict is inconclusive. Otherwise each model gets a Brier score, `(confidence - correct)^2`.
- **Narration:** the demo voiceover was generated with ElevenLabs text-to-speech. That is a closed service used only for narration; the predictions come from open-weight models running locally.

## Why Open Innovation Matters

A claim about the physical world is only worth something if someone else can test it. With open-weight models, anyone can run the same prompt on their own machine, see the raw samples, and go outside and check. I could see the individual samples behind each prediction, and that mattered: on an earlier draft of the place descriptions, `llama3.2:3b` picked one place in a first run and the other place in a second run with more samples. A hosted model behind an API would hide that instability. The tool is re-runnable by design: two places, the models you choose, a phone.

## What I Found

**Predictions, locked before measuring** (`predictions.json`, 7 samples each). `qwen3:4b` picked Main Street as quieter in 7 of 7 samples (confidence 0.77). `llama3.2:3b` also picked Main Street in 7 of 7 (confidence 0.79). Both models agree, so this experiment cannot rank them on accuracy; it can only show whether their shared prediction was right.

**Honest note on reruns.** My first predictions used a draft of place B that did not match the place I actually measure (the metro station entrance instead of the convenience shop), so I discarded them and reran with the real descriptions before going outside. The earlier runs are in the git history. On that earlier draft `llama3.2:3b` flipped between runs, which is the instability noted above.

[Measured results: A level, B level, within-place spread, verdict, Brier scores.]

## Limitations

- One uncalibrated phone microphone, relative dBFS, not dB(A). Only comparisons within one session on one device mean anything.
- My two places are far apart, so the runs at each place happen at different times. Time of day can explain part of any gap. The tool prints the time between the runs and I note it in the results.
- Wind, traffic and weather are logged, not corrected.
- One experiment is one data point. Two models and one pair of places cannot say which model is better. The tool is built to avoid declaring a winner from one run.

## Related work

Forecasting benchmarks such as [ForecastBench](https://arxiv.org/abs/2409.19839) score models on future events, and [SciPredict](https://arxiv.org/abs/2604.10718) scores them on outcomes of published experiments. I did not find one that uses a measurement the builder takes in the field as ground truth, but my search was limited.
