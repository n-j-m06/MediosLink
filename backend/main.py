from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Load emotion classification model
emotion_analyzer = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

class TextPayload(BaseModel):
    paragraph: str

@app.post("/analyze-mood")
async def analyze_mood(payload: TextPayload):
    text = payload.paragraph

    # Get emotion predictions
    raw_predictions = emotion_analyzer(text)[0]

    # Count sentences
    sentence_count = (
        text.count('.') +
        text.count('!') +
        text.count('?')
    )

    character_count = len(text)
    avg_sentence_length = character_count / max(sentence_count, 1)

    # Sort emotions by confidence
    sorted_emotions = sorted(
        raw_predictions,
        key=lambda x: x["score"],
        reverse=True
    )

    primary_mood = sorted_emotions[0]["label"]
    confidence = round(sorted_emotions[0]["score"], 3)

    # Audio intensity logic
    if avg_sentence_length < 30 or "!" in text:
        intensity = "high"
    elif avg_sentence_length > 80:
        intensity = "low"
    else:
        intensity = "normal"

    return {
        "mood": primary_mood,
        "confidence": confidence,
        "audio_modifiers": {
            "intensity": intensity,
            "average_sentence_length": round(avg_sentence_length, 2),
            "all_scores": {
                item["label"]: round(item["score"], 3)
                for item in sorted_emotions
            }
        }
    }