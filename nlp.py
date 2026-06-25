from transformers import pipeline
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("valhalla/t5-base-qg-hl")
model = AutoModelForSeq2SeqLM.from_pretrained("valhalla/t5-base-qg-hl")
# qg_pipeline = pipeline(
#     "text2text-generation",
#     model="valhalla/t5-base-qg-hl"
# )

def clean_sentence(sentence):
    sentence = sentence.strip()

    # remove repeated words like "Dr Dr Dr"
    sentence = re.sub(r'\b(\w+)( \1\b)+', r'\1', sentence)

    # remove extra spaces
    sentence = re.sub(' +', ' ', sentence)

    return sentence

def generate_questions(text):

    flashcards = []

    # split properly (not only ".")
    sentences = re.split(r'[.\n]', text)

    seen = set()

    for sentence in sentences:

        sentence = clean_sentence(sentence)

        # skip small / garbage
        if len(sentence) < 10:
            continue

        # remove duplicates
        if sentence in seen:
            continue
        seen.add(sentence)

        try:
            input_text = "generate question: " + sentence

            result = qg_pipeline(
                input_text,
                max_length=64,
                do_sample=False
            )

            question = result[0]["generated_text"].strip()

            # FORCE QUESTION FORMAT
            if not question.endswith("?"):
                question = "What is: " + sentence[:25] + "?"

            flashcards.append({
                "question": question,
                "answer": sentence
            })

        except Exception as e:
            print("Error:", e)

    return flashcards