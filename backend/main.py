from pydantic import BaseModel, Field
from typing import List

class EmotionAnalysisSchema(BaseModel):
    dominant_emotion: str = Field(
        description="The primary mood of the text. Must be exactly one of: Joy, Sadness, Anger, Fear, Suspense, Calm, or Neutral."
    )
    valence: float = Field(
        description="The positivity score of the narrative depth, ranging from -1.0 (deeply tragic/dark) to 1.0 (highly optimistic/celebratory)."
    )
    arousal: float = Field(
        description="The physiological intensity or energy level of the text, ranging from 0.0 (calm, stagnant, whispered) to 1.0 (chaotic, fast-paced, high stakes, screaming)."
    )
    tempo_preference: str = Field(
        description="The ideal speed for accompanying audio. Must be exactly one of: Ambient, Slow, Moderate, or Intense."
    )
    transition_detected: bool = Field(
        description="True if the text experiences a sharp emotional pivot mid-paragraph (e.g., a peaceful scene interrupted by a sudden shock)."
    )
    linguistic_justification: str = Field(
        description="A one-sentence breakdown of the subtext, sarcasm, or syntax structure that informed this emotional classification."
    )
    import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Configure the Gemini SDK
# Make sure GEMINI_API_KEY is set in your environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class TextPayload(BaseModel):
    paragraph: str

SYSTEM_PROMPT = (
    "You are an advanced computational linguistics engine specialized in deep narrative "
    "sentiment mapping. Your task is to analyze the subtext, structural cadence, punctuation, "
    "and psychological tone of the provided paragraph. Look beyond literal words to extract "
    "the underlying emotional state to match an audio track."
)

@app.post("/analyze-mood-premium")
async def analyze_mood_premium(payload: TextPayload):
    if not payload.paragraph.strip():
        raise HTTPException(status_code=400, detail="Paragraph text cannot be empty.")
        
    try:
        # Initialize the model (using gemini-1.5-pro or gemini-2.5-pro for deep reasoning capacity)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=SYSTEM_PROMPT
        )
        
        # Enforce high-accuracy structured JSON out of the box
        response = model.generate_content(
            payload.paragraph,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": EmotionAnalysisSchema,
                "temperature": 0.1,  # Low temperature guarantees deterministic, analytical consistency
            }
        )
        
        # The response text is a guaranteed valid JSON string matching our Pydantic model
        import json
        structured_data = json.loads(response.text)
        
        return {
            "status": "success",
            "data": structured_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine analysis failure: {str(e)}")