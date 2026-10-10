# Week 1 submit checklist (fast path, about 45 minutes)

Deadline: October 11, 11:59 PM PDT. Only your first submitted entry is judged, so post once, when complete.

## 1. Pick two places (2 min)
Two real places you can walk between. Write 2–3 plain sentences for each (street type, traffic, shops, trees). Same level of detail for both.

## 2. Get the model predictions (3 min)
Models `qwen3:4b` and `llama3.2:3b` are pulled locally. Start the server if it is not running:

```bash
ollama serve
```

Then in another terminal:

```bash
cd /home/ottodev/prove-it-outside
python3 run_models.py --models qwen3:4b llama3.2:3b \
  --desc-a "DESCRIPTION OF A" --desc-b "DESCRIPTION OF B" \
  --when "today, time, weather" --samples 5
```

Paste the JSON output into step 1 of `index.html`, then click Lock predictions BEFORE you go out.

## 3. Measure (15 min)
Open `index.html` in Chrome. Stand at A for 30 s, then B for 30 s, then A and B again. Same phone, same posture. Fill in the conditions box. Click Score, then Export JSON.

## 4. Record the demo (5 min)
Screen-record the page: prompt, predictions locked, the four measurements, the score. Add one photo of you at a place.

## 5. Repo (5 min)
```bash
cd /home/ottodev/prove-it-outside
git init && git add -A && git commit -m "Prove It Outside"
```
Create a GitHub repo and push. Add the exported run JSON.

## 6. Post (10 min)
Fill the brackets in `DEV_POST.md`: model names and how you ran them, results, demo link, repo link. Publish on DEV with tags `#devchallenge` and `#hf26challenge`.

If the measurement comes out inconclusive, say so in "What I Found". That is a valid result and the tool is designed to report it.
