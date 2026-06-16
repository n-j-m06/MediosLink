# ⚙️ MediosLink Backend

## Overview

The MediosLink backend serves as the intelligence engine responsible for emotion detection, narrative understanding, soundtrack recommendation, and music metadata generation.

Built using FastAPI and HuggingFace Transformers, the backend processes textual narratives and returns emotionally aligned soundtrack recommendations.

---

## Core Responsibilities

### Emotion Classification

Uses:

```text
SamLowe/roberta-base-go_emotions
```

to identify emotional signals present within textual narratives.

---

### NRC Emotion Lexicon Processing

The NRC Emotion Intensity Lexicon provides supplementary emotion scores that improve prediction robustness.

Supported Lexicon Emotions:

* Joy
* Sadness
* Anger
* Fear
* Anticipation

---

### Hybrid Emotion Detection

Combines:

* Transformer Predictions
* Lexicon Analysis
* Rule-Based Detection

to identify:

* Romantic Narratives
* Fear-Based Narratives
* Calm Narratives
* Suspense Narratives

---

### Musical Recommendation Engine

Generates:

* Soundtrack Style
* Instrument Suggestions
* Tempo Recommendations
* BPM Values
* Audio Recommendations

---

## Available Soundtrack Categories

### Joy

* Uplifting Theme
* Celebration Theme
* Victory Theme

### Romantic

* Gentle Strings
* Romantic Piano
* Love Theme

### Sadness

* Emotional Piano
* Lonely Night
* Heartbreak Theme

### Fear

* Suspense Build
* Danger Theme
* Dark Horror
* Thriller Chase

### Calm

* Ambient Forest
* Peaceful River
* Meditation Theme

### Action

* Battle Drums
* Intense Action
* Rage Theme

### Surprise

* Discovery
* Mystery Theme
* Reveal Theme
* Wonder Theme

---

## API Endpoint

### Analyze Narrative

```http
POST /analyze-mood-premium
```

### Sample Request

```json
{
  "paragraph": "I hugged my girlfriend and felt the warmth of her love."
}
```

### Sample Response

```json
{
  "status": "success",
  "data": {
    "dominant_emotion": "Romantic",
    "confidence": 95.1,
    "bgm_intensity": "Medium",
    "valence": 0.9,
    "arousal": 0.9,
    "tempo_preference": "Intense",
    "transition_detected": false,
    "bgm_style": "Love Theme",
    "instrument": "Piano + Violin",
    "tempo_bpm": 150,
    "recommended_bgm": "http://127.0.0.1:8000/bgm/romantic/love_theme.mp3"
  }
}
```

---

## Running Backend

```bash
pip install -r requirements.txt

uvicorn main:app --reload
```
