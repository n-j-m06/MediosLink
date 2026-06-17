from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from fastapi.staticfiles import StaticFiles
import re
import random
app = FastAPI()
app.mount(
    "/bgm",
    StaticFiles(directory="bgm"),
    name="bgm"
)
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

            if line.startswith("word"):
                continue

            parts = line.strip().split("\t")

            if len(parts) != 3:
                continue

            word, emotion, intensity = parts

            try:
                intensity = float(intensity)
            except ValueError:
                continue

            lexicon.setdefault(word, {})
            lexicon[word][emotion] = intensity

    return lexicon
print("Backend Started")

try:
    emotion_lexicon = load_nrc_lexicon()
    print(f"NRC loaded with {len(emotion_lexicon)} words")
except Exception as e:
    print(f"Failed to load NRC lexicon: {e}")
    emotion_lexicon = {}

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
        "neutral"
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


def hybrid_emotion_detection(text, model_emotion):

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

    words = set(
        re.findall(
            r"\b[a-zA-Z]+\b",
            text.lower()
        )
    )

    romantic_words = {
        "love","lover","romance","romantic",
        "kiss","hug","cuddle","marriage",
        "wedding","girlfriend","boyfriend",
        "wife","husband","soulmate",
        "sweetheart","darling"
    }

    fear_words = {
        "fear","afraid","terror","threat",
        "danger","dead","death","murder",
        "killer","horror","panic","scared",
        "attack","kidnap","blood"
    }

    calm_words = {
        "peace","peaceful","calm","serene",
        "tranquil","ocean","lake","forest",
        "nature","sunset","sunrise",
        "breeze","relax","meditation"
    }

    if words & romantic_words:
        return "Romantic"

    if words & fear_words:
        return "Fear"

    if len(words & calm_words) >= 2:
        return "Calm"

    if scores[dominant_nrc] > 1.2:
        return nrc_mapping.get(
            dominant_nrc,
            model_emotion
        )

    return model_emotion


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
    if words & fear_words:
      return "Fear"

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
def get_bgm_intensity(confidence):

    if confidence < 40:
        return "Soft"

    elif confidence < 75:
        return "Medium"

    return "Intense"
def get_bgm_style(emotion):

    styles = {
        "Joy": "Inspirational",
        "Sadness": "Emotional",
        "Anger": "Action",
        "Fear": "Horror",
        "Suspense": "Thriller",
        "Calm": "Ambient",
        "Romantic": "Love Theme",
        "Neutral": "Background"
    }

    return styles.get(emotion, "Background")
def get_instrument(emotion):

    instruments = {
        "Joy": "Piano + Strings",
        "Sadness": "Solo Piano",
        "Anger": "Drums + Brass",
        "Fear": "Dark Strings",
        "Suspense": "Synth Pulses",
        "Calm": "Pads + Flute",
        "Romantic": "Piano + Violin",
        "Neutral": "Soft Pads"
    }

    return instruments.get(emotion, "Soft Pads")
def get_bpm(arousal):

    return int(60 + (arousal * 100))

def recommend_bgm(emotion, intensity):

    bgm_library = {

        "Joy": {
            "Soft": ["Joy/uplifting_theme.mp3"],
            "Medium": ["Joy/celebration_theme.mp3"],
            "Intense": ["Joy/victory_theme.mp3"]
        },

        "Romantic": {
            "Soft": ["romantic/gentle_strings.mp3"],
            "Medium": ["romantic/romantic_piano.mp3"],
            "Intense": ["romantic/love_theme.mp3"]
        },

        "Sadness": {
            "Soft": [
                "sadness/emotional_piano.mp3",
                "sadness/lonely_night.mp3"
            ],
            "Medium": [
                "sadness/sad_strings.mp3"
            ],
            "Intense": [
                "sadness/heartbreak_theme.mp3"
            ]
        },

        "Fear": {
            "Soft": [
                "fear/suspense_build.mp3"
            ],
            "Medium": [
                "fear/danger_theme.mp3"
            ],
            "Intense": [
                "fear/dark_horror.mp3",
                "fear/thriller_chase.mp3"
            ]
        },

        "Suspense": {
            "Soft": [
                "surprise/discovery.mp3"
            ],
            "Medium": [
                "surprise/mystery_theme.mp3",
                "surprise/wonder_theme.mp3"
            ],
            "Intense": [
                "surprise/reveal_theme.mp3"
            ]
        },

        "Calm": {
            "Soft": [
                "calm/ambient_forest.mp3"
            ],
            "Medium": [
                "calm/peaceful_river.mp3"
            ],
            "Intense": [
                "calm/meditation_theme.mp3"
            ]
        },

        "Anger": {
            "Soft": [
                "action/battle_drums.mp3"
            ],
            "Medium": [
                "action/intense_action.mp3"
            ],
            "Intense": [
                "action/rage_theme.mp3"
            ]
        }
    }

    try:
        return random.choice(
            bgm_library[emotion][intensity]
        )
    except:
        return "default/default.mp3"



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

        confidence = round(
            top_emotion["score"] * 100,
            2
        )

        bgm_intensity = get_bgm_intensity(
            confidence
        )

        transition_words = [
            "but", "however", "although", "though",
            "yet", "still", "nevertheless",
            "suddenly", "unexpectedly", "meanwhile",
            "later", "eventually", "instead",
            "fortunately", "unfortunately",
            "despite", "until", "when", "once",
            "all of a sudden",
            "to his surprise",
            "to her surprise"
        ]

        transition_detected = any(
            phrase in payload.paragraph.lower()
            for phrase in transition_words
        )

        result = {
            "dominant_emotion": dominant_emotion,
            "confidence": confidence,
            "bgm_intensity": bgm_intensity,
            "valence": round(valence, 2),
            "arousal": round(arousal, 2),
            "tempo_preference": get_tempo(arousal),
            "transition_detected": transition_detected,
            "bgm_style": get_bgm_style(dominant_emotion),
            "instrument": get_instrument(dominant_emotion),
            "tempo_bpm": get_bpm(arousal),
            "recommended_bgm":
                    f"/bgm/{recommend_bgm(dominant_emotion, bgm_intensity)}"
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