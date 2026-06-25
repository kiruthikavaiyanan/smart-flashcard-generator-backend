from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re

from db import flashcards_collection
from nlp import generate_questions

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Note(BaseModel):
    text: str


@app.get("/")
def root():
    return {
        "message": "Smart Flashcard Generator API is running"
    }


# 🔥 Generate flashcards (NO duplicates + cleaned text)
@app.post("/generate-flashcards")
def generate_flashcards(note: Note):

    # ✅ CLEAN TEXT (VERY IMPORTANT)
    text = re.sub(r'\s+', ' ', note.text.strip().lower())
    text = re.sub(r'[^\w\s]', '', text)

    # 🔍 duplicate check
    existing = flashcards_collection.find_one({"input_text": text})

    if existing:
        existing["_id"] = str(existing["_id"])
        return {
            "message": "Flashcards already exist",
            "flashcards": existing["flashcards"],
            "id": existing["_id"]
        }

    # 🤖 generate flashcards
    flashcards = generate_questions(note.text)

    # 💾 save to MongoDB
    result = flashcards_collection.insert_one({
        "input_text": text,
        "flashcards": flashcards
    })

    return {
        "message": "Flashcards generated successfully",
        "id": str(result.inserted_id),
        "flashcards": flashcards
    }


# 📚 Get all flashcards (history sidebar)
@app.get("/flashcards")
def get_flashcards():

    data = list(
        flashcards_collection.find().sort("_id", -1)
    )

    for item in data:
        item["_id"] = str(item["_id"])

    return data


# 🗑️ DELETE ALL HISTORY (clear system)
@app.delete("/delete-all-flashcards")
def delete_all_flashcards():

    result = flashcards_collection.delete_many({})

    return {
        "message": "All flashcards deleted successfully",
        "deleted_count": result.deleted_count
    }


# 🧪 MongoDB test
@app.get("/test-db")
def test_db():

    try:
        flashcards_collection.insert_one({"name": "test"})
        return {
            "message": "MongoDB Connected Successfully"
        }

    except Exception as e:
        return {
            "error": str(e)
        }