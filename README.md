# 🎬 MediosLink – AI-Powered Cinematic Soundtrack Recommendation System

## 📖 Overview

MediosLink is an AI-driven narrative analysis and soundtrack recommendation platform designed to bridge the gap between storytelling and music composition.

The system analyzes user-provided stories, scripts, narratives, and textual content using advanced Natural Language Processing techniques and automatically recommends emotionally appropriate background music (BGM) to enhance the storytelling experience.

By combining transformer-based emotion detection, lexicon-driven sentiment analysis, narrative transition recognition, and soundtrack intelligence, MediosLink acts as an AI Music Director capable of translating textual emotions into immersive cinematic soundscapes.

---

## 🎯 Problem Statement

Content creators, filmmakers, storytellers, podcasters, game developers, and scriptwriters often struggle to identify suitable background music that matches the emotional progression of a narrative.

Traditional soundtrack selection requires:

* Manual review of scripts
* Music expertise
* Extensive soundtrack libraries
* Significant creative effort

MediosLink automates this process by intelligently analyzing the emotional context of narratives and recommending suitable cinematic soundtracks.

---

## 🚀 Key Features

### 🧠 AI-Powered Emotion Detection

Utilizes the HuggingFace GoEmotions Transformer Model to identify emotions present within textual narratives.

### 📚 NRC Emotion Intensity Lexicon Integration

Enhances transformer predictions using the NRC Emotion Intensity Lexicon, allowing more robust emotion understanding.

### 🔀 Hybrid Emotion Classification

Combines:

* Transformer Predictions
* Lexicon Scores
* Rule-Based Narrative Understanding

to improve classification accuracy.

### ❤️ Specialized Narrative Detection

Custom logic for detecting:

* Romantic Narratives
* Fear-Based Narratives
* Calm and Peaceful Narratives
* Suspense-Oriented Narratives

### 🎵 Dynamic Soundtrack Recommendation

Automatically recommends background music based on:

* Emotion
* Intensity
* Narrative Context

### 🎼 Musical Attribute Generation

Generates:

* BGM Style
* Instrument Suggestions
* Tempo Recommendations
* BPM Estimation

### 🎬 Director's Note

Provides an AI-generated cinematic explanation describing why a particular soundtrack recommendation is appropriate.

### 🎧 Real-Time Audio Playback

Users can instantly preview recommended soundtracks directly within the application.

---

## 🧩 System Architecture

```text
User Story Input
        │
        ▼
Emotion Analysis
(HuggingFace GoEmotions)
        │
        ▼
NRC Lexicon Processing
        │
        ▼
Hybrid Emotion Classification
        │
        ▼
Narrative Transition Detection
        │
        ▼
Musical Feature Generation
        │
        ▼
Soundtrack Recommendation Engine
        │
        ▼
Audio Playback & Visualization
```

---

## 🛠 Technology Stack

### Frontend

* React
* Vite
* Tailwind CSS v4
* Framer Motion
* Axios
* Lucide React

### Backend

* FastAPI
* HuggingFace Transformers
* PyTorch
* NRC Emotion Intensity Lexicon
* Python

### AI Components

* GoEmotions Transformer Model
* Lexicon-Based Sentiment Analysis
* Rule-Based Emotion Refinement
* Music Recommendation Logic

---

## 📂 Project Structure

```text
MediosLink/
│
├── frontend/
│
├── backend/
│
├── README.md
│
├── requirements.txt
│
└── .gitignore
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
cd MediosLink
```

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## 📈 Future Enhancements

* Multi-Emotion Story Tracking
* Emotion Timeline Visualization
* Custom Soundtrack Uploads
* Genre-Based Recommendations
* AI Music Generation
* Story-to-Film Scoring Assistance

---

## 👨‍💻 Developed By

MediosLink Development Team

An AI-powered storytelling and soundtrack recommendation platform designed to enhance cinematic narrative experiences.
