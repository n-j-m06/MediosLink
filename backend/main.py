import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI application
app = FastAPI(title="AI Writing Assistant: Mood Engine Backend")

# Enable CORS so your frontend application can talk to it safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the NLP pipeline globally so it loads once when the server boots
print("Initializing Hugging Face Emotion Model...")
# A robust, standard dataset model for multi-emotion detection
emotion_classifier = pipeline(
    "text-classification", 
    model="SamLowe/roberta-base-go_emotions", 
    top_k=None
)
print("Model ready!")

# Define the structure of incoming requests from the text editor
class ParagraphRequest(BaseModel):
    text: str

# Define a baseline threshold for shifting states
CONFIDENCE_THRESHOLD = 0.20

@app.post("/api/analyze-mood")
async def analyze_mood(payload: ParagraphRequest):
    """
    Receives text, runs emotion classification, maps scores, 
    and returns instructions to the frontend.
    """
    if not payload.text.strip():
        return {"status": "empty", "mood": "neutral", "scores": {}}

    try:
        # Run emotion classification asynchronously in a real app context
        # payload.text corresponds to a paragraph sent on an Enter keypress or a debounce timeout
        raw_predictions = emotion_classifier(payload.text)[0]
        
        # Convert predictions to a cleaner key-value dictionary
        # Example output format: {"joy": 0.85, "sadness": 0.02, ...}
        scores_dict = {item['label']: round(item['score'], 4) for item in raw_predictions}
        
        # Determine the top detected emotion label
        top_prediction = max(raw_predictions, key=lambda x: x['score'])
        detected_mood = top_prediction['label']
        confidence = top_prediction['score']
        
        # fallback rule: if confidence is incredibly low, maintain neutral track
        if confidence < CONFIDENCE_THRESHOLD:
            detected_mood = "neutral"

        # Construct payload instructions for the frontend audio layer
        return {
            "status": "success",
            "primary_mood": detected_mood,
            "confidence": confidence,
            "all_scores": scores_dict
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    # Start server locally on port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)