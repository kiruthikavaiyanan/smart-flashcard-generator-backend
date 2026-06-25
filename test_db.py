from db import flashcards_collection

try:
    flashcards_collection.insert_one({
        "name": "test"
    })

    print("MongoDB Connected Successfully")

except Exception as e:
    print("Error:", e)