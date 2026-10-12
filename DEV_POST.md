*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built

AI models will tell you things about places they have never been. The only way to check one of those claims is to go there. **Prove It Outside** makes that check the whole point.

An open-weight model must commit to a falsifiable prediction about the physical world: *which of two places is quieter?* The prediction and the model's confidence are locked first. Then someone goes out, records sound at both places, and the tool scores each model with a Brier score. If the measurements are too noisy to tell the two places apart, the tool says **inconclusive** and refuses to score anyone.

It is for anyone curious whether an AI's confident guess about a place survives a microphone, and it works with any open model you can ask a question.

**What I tested for this entry:** a street in the city versus a McDonald's restaurant, using sound recorded with a phone voice recorder. [CONFIRM: I recorded these myself at ___ on 12 October 2026.] The tool also has a live mode that reads the phone microphone directly; I did not have time to run a live field session, so this entry's results come from recordings made with a phone voice recorder app and analyzed from the files. The tool labels this on screen, in the export and in the score.

## Demo

Try it: https://otto-deviant1904.github.io/prove-it-outside/

Enter two places, add each model's prediction, lock them, then either measure live with your phone's microphone or analyze recordings. Nothing is uploaded; everything runs in your browser.

## Code

https://github.com/Otto-Deviant1904/prove-it-outside

- `index.html`: the whole tool, one file, no build step, no network calls.
- `run_models.py`: asks local Ollama models the same prompt several times and prints predictions.
- `predictions.json` and `predictions_command.txt`: the exact predictions and the command that produced them, committed in git (`bc63e42`) before the recordings were analyzed with the tool.

## How I Built It

- **Open models:** `qwen3:4b` and `llama3.2:3b`, both open-weight, run locally with Ollama. Each got the same one-line description of each place (A: "A street in the city." B: "A McDonald's restaurant."), seven samples at temperature 0.7. A model's pick is its majority vote. Its confidence is the mean implied probability that the pick is right across all samples, so dissenting samples pull it down.
- **Measurement:** in live mode the Web Audio API reads the phone microphone for 30 seconds with echo cancellation, noise suppression and auto-gain switched off. In recording mode it decodes an audio file and analyzes 30 s or 15 s segments. Either way, the level of a run is the energy-averaged level in dBFS, which matches the question the models were asked ("lower average sound level"). Live runs shorter than 27 seconds or with silent audio are discarded. A recording needs a source label, which is saved with the results.
- **Scoring:** each place needs at least two runs. If the spread between runs at one place is as large as the gap between places, the verdict is inconclusive. Otherwise each model gets a Brier score, `(confidence - correct)^2`.
- **Narration:** the original demo voiceover used ElevenLabs text-to-speech. That is a closed service used only for narration; the predictions come from open-weight models running locally.

## What I Found

**Predictions, locked before the analysis** (`predictions.json`, 7 samples each): `qwen3:4b` picked the McDonald's as quieter in 7 of 7 samples (confidence 0.83). `llama3.2:3b` picked the street in 5 of 7 (confidence 0.66). The two models disagree.

**Measured:** [RESULTS: level of each recording, the street runs versus the McDonald's runs, within-place spread, the verdict, and each model's Brier score.]

**Honest notes**
- My first predictions were for other place descriptions (Main Street in front of a college versus a convenience shop near a metro station) that did not match the recordings I ended up with. I discarded them and reran with descriptions that match. They are in `history/` and in the git history.
- I had looked at the rough loudness of the recordings before the models were rerun. The models never see audio and I did not change the prompt after seeing it, but this is not blind.
- My McDonald's recording is about 31 seconds, so for the second run at each place the tool used two 15 second segments from the same recording. Segments of one recording are not independent visits, so the repeatability check is weaker than with separate visits.

## Why Does Open Innovation Matter?

A claim about the physical world is only worth something if someone else can test it. With open-weight models anyone can run the same prompt on their own machine, see the raw samples, and go outside and check. That mattered here: on an earlier draft of the place descriptions, `llama3.2:3b` picked one place in a first run and the other place in a second run with more samples. A hosted model behind an API would hide that instability. Here I could see every sample, so the tool reports a confidence that reflects the disagreement.

## Limitations

- One uncalibrated phone microphone, relative dBFS, not dB(A). Recordings made with different gain or equipment are not truly comparable.
- Wind, traffic and time of day are not controlled.
- One experiment is one data point. Two models and one pair of places cannot say which model is better. The tool is built to avoid declaring a winner from one run.
