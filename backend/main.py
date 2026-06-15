from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import re
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def load_nrc_lexicon():

    lexicon = {}

    with open(
        "NRC-Emotion-Intensity-Lexicon-v1.txt",
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            parts = line.strip().split("\t")

            if len(parts) != 3:
                continue

            word, emotion, intensity = parts

            try:
                intensity = float(intensity)
            except:
                continue

            if word not in lexicon:
                lexicon[word] = {}

            lexicon[word][emotion] = intensity

    return lexicon


emotion_lexicon = {}

print("Backend Started")

print(
    "NRC loaded with {len(emotion_lexicon)} words"
)
# Load model once during startup
emotion_classifier = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=None
)


class TextPayload(BaseModel):
    paragraph: str


def map_emotion(emotion):

    emotion = emotion.lower()

    joy_group = [
        "joy",
        "gratitude",
        "love",
        "admiration",
        "approval",
        "optimism",
        "pride",
        "relief",
        "amusement"
    ]

    sadness_group = [
        "sadness",
        "grief",
        "remorse",
        "disappointment"
    ]

    anger_group = [
        "anger",
        "annoyance",
        "disapproval"
    ]

    fear_group = [
        "fear",
        "nervousness"
    ]

    suspense_group = [
        "surprise",
        "realization",
        "confusion",
        "curiosity"
    ]

    calm_group = [
        "caring",
        "approval",
        "admiration"
    ]

    if emotion in joy_group:
        return "Joy"

    if emotion in sadness_group:
        return "Sadness"

    if emotion in anger_group:
        return "Anger"

    if emotion in fear_group:
        return "Fear"

    if emotion in suspense_group:
        return "Suspense"

    if emotion in calm_group:
        return "Calm"

    return "Neutral"

def nrc_emotion_score(text):

    scores = {
        "anger": 0,
        "fear": 0,
        "joy": 0,
        "sadness": 0,
        "anticipation": 0
    }

    words = re.findall(
        r"\b[a-zA-Z]+\b",
        text.lower()
    )

    for word in words:

        if word not in emotion_lexicon:
            continue

        for emotion, intensity in emotion_lexicon[word].items():

            if emotion in scores:
                scores[emotion] += intensity

    return scores

def hybrid_emotion_detection(
    text,
    model_emotion
):

    scores = nrc_emotion_score(text)

    dominant_nrc = max(
        scores,
        key=scores.get
    )

    nrc_mapping = {
        "joy": "Joy",
        "sadness": "Sadness",
        "anger": "Anger",
        "fear": "Fear",
        "anticipation": "Suspense"
    }

    romantic_words = {
        "love","lover","romance","romantic",
        "kiss","hug","cuddle","marriage",
        "wedding","girlfriend","boyfriend",
        "wife","husband","soulmate",
        "sweetheart","darling"
    }

    calm_words = {
        "peace","peaceful","calm","serene",
        "tranquil","ocean","lake","forest",
        "nature","sunset","sunrise",
        "breeze","relax","meditation"
    }

    words = set(
        re.findall(
            r"\b[a-zA-Z]+\b",
            text.lower()
        )
    )

    if words & romantic_words:
        return "Romantic"

    if len(words & calm_words) >= 2:
        return "Calm"

    if scores[dominant_nrc] > 1.2:
        return nrc_mapping.get(
            dominant_nrc,
            model_emotion
        )

    return model_emotion

def get_valence(emotion):
    positive = {
        "Joy": 0.8,
        "Calm": 0.5,
        "Romantic": 0.9
    }

    negative = {
        "Sadness": -0.8,
        "Fear": -0.7,
        "Anger": -0.9,
        "Suspense": -0.3
    }

    if emotion in positive:
        return positive[emotion]

    if emotion in negative:
        return negative[emotion]

    return 0.0


def get_arousal(emotion):
    values = {
        "Joy": 0.8,
        "Anger": 0.95,
        "Fear": 0.9,
        "Suspense": 0.85,
        "Sadness": 0.4,
        "Calm": 0.2,
        "Neutral": 0.3,
        "Romantic": 0.9
    }

    return values.get(emotion, 0.3)


def get_tempo(arousal):
    if arousal < 0.25:
        return "Ambient"

    if arousal < 0.5:
        return "Slow"

    if arousal < 0.75:
        return "Moderate"

    return "Intense"


@app.post("/analyze-mood-premium")
async def analyze_mood_premium(payload: TextPayload):

    if not payload.paragraph.strip():
        raise HTTPException(
            status_code=400,
            detail="Paragraph text cannot be empty."
        )

    try:

        predictions = emotion_classifier(payload.paragraph)[0]

        top_emotion = max(
            predictions,
            key=lambda x: x["score"]
        )

        model_emotion = map_emotion(
        top_emotion["label"]
        )

        dominant_emotion = hybrid_emotion_detection(
        payload.paragraph,
        model_emotion
    )

        valence = get_valence(
            dominant_emotion
        )

        arousal = get_arousal(
            dominant_emotion
        )

        transition_detected = any(
            word in payload.paragraph.lower()
            for word in [
                "suddenly",
                "however",
                "but",
                "unexpectedly",
                "meanwhile"
            ]
        )

        result = {
            "dominant_emotion": dominant_emotion,
            "valence": round(valence, 2),
            "arousal": round(arousal, 2),
            "tempo_preference": get_tempo(arousal),
            "transition_detected": transition_detected,
            "linguistic_justification":
                f"Detected dominant emotional signal '{top_emotion['label']}' "
                f"with confidence {round(top_emotion['score'] * 100, 2)}%."
        }

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

