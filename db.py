from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://vkiruthika69_db_user:keerthi_1234@kiruthika.8zietpa.mongodb.net/?retryWrites=true&w=majority&appName=kiruthika"


client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

db = client["flashcards_db"]

flashcards_collection = db["flashcards"]
users_collection = db["users"]
