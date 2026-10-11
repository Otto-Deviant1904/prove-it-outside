# Week 1 submit checklist

Deadline: Sunday October 11, 11:59 PM PDT (Monday October 12, about 5:59 PM AEDT). Only your first submitted entry is judged, so post once, when complete.

Already done: repo is public, models pulled, predictions made and committed (`predictions.json`, command in `predictions_command.txt`), demo voiceover generated (`demo_voiceover.mp3`).

## 1. Open the tool on your phone (2 min)
Open the https link on your phone (GitHub Pages): https://otto-deviant1904.github.io/prove-it-outside/
The microphone only works on a secure page, so do not use a local network address. If the page says the microphone API is unavailable, you opened an insecure link.

In step 2, name place A `Main Street` and place B `Convenience shop`. Add the two models and their answers from `predictions.json`: `qwen3:4b`, A is quieter, 77. `llama3.2:3b`, A is quieter, 79. (Or open "Paste JSON" and paste the whole file.) Tap **Lock predictions** BEFORE you leave.

## 2. Measure (about 10 min at each place)
Keep the screen on and the page visible for the whole 30 seconds. If the screen sleeps, the run is discarded.
- At Main Street, in front of the college: two runs. Same posture each time: stand still, phone at chest height, mic facing the same way.
- At the convenience shop near the metro station: two runs.
- Fill the Conditions box before each run (time, wind, weather, traffic). Do the pair of runs at one place back to back.
- Tap **Score predictions**, then **Export JSON**.

If the Score says INCONCLUSIVE, that is a valid result. Report it as it is.

## 3. Record the demo (5 min)
Screen-record the page: prompt, locked predictions, the four measurements, the score. Lay `demo_voiceover.mp3` over it, or record your own. Add one photo of you at a place if you like.

## 4. Send the results to Claude (or fill the post yourself)
Send the exported JSON. The post needs: the measured levels, the verdict, the Brier scores, the demo link.

## 5. Post (10 min)
Fill the bracketed parts of `DEV_POST.md`. Publish on DEV with tags `#devchallenge` and `#hf26challenge`, the demo, and the repo link.
