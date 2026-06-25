from transformers import pipeline
import re

# Load Question Generation Model
qg_pipeline = pipeline(
    "text2text-generation",
    model="valhalla/t5-base-qg-hl",
    tokenizer="valhalla/t5-base-qg-hl"
)


def clean_sentence(sentence):
    sentence = sentence.strip()

    # Remove repeated words
    sentence = re.sub(r'\b(\w+)( \1\b)+', r'\1', sentence)

    # Remove extra spaces
    sentence = re.sub(r'\s+', ' ', sentence)

    return sentence


def generate_questions(text):

    flashcards = []

    # Split text into sentences
    sentences = re.split(r'[.\n]', text)

    seen = set()

    for sentence in sentences:

        sentence = clean_sentence(sentence)

        # Skip short sentences
        if len(sentence) < 10:
            continue

        # Skip duplicates
        if sentence in seen:
            continue

        seen.add(sentence)

        try:
            input_text = f"generate question: {sentence}"

            result = qg_pipeline(
                input_text,
                max_length=64,
                do_sample=False
            )

            question = result[0]["generated_text"].strip()

            # Fallback question
            if not question.endswith("?"):
                question = f"What is {sentence[:30]}?"

            flashcards.append({
                "question": question,
                "answer": sentence
            })

        except Exception as e:
            print("Question Generation Error:", e)

    return flashcards