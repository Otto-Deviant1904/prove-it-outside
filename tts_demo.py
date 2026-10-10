#!/usr/bin/env python3
"""Generate a demo voiceover with ElevenLabs.

Reads the API key from the ELEVEN_API_KEY environment variable (never stored in files).

Usage:
  ELEVEN_API_KEY=... python3 tts_demo.py demo_script.txt demo_voiceover.mp3
"""
import json, os, sys, urllib.error, urllib.request

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs "Rachel" premade voice
MODEL = "eleven_multilingual_v2"


def main():
    key = os.environ.get("ELEVEN_API_KEY")
    if not key:
        sys.exit("Set ELEVEN_API_KEY in the environment.")
    text = open(sys.argv[1], encoding="utf-8").read().strip()
    body = json.dumps({"text": text, "model_id": MODEL}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        body,
        {"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            audio = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")
    with open(sys.argv[2], "wb") as f:
        f.write(audio)
    print(f"wrote {sys.argv[2]} ({len(audio)} bytes)")


if __name__ == "__main__":
    main()
