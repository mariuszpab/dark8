import json

import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

MODEL_DIR = "C:/DARK8_MARK01/dark8_mark01/nlp/models/intent_onnx"

# Wczytanie etykiet
with open(f"{MODEL_DIR}/labels.json", "r", encoding="utf-8") as f:
    LABELS = json.load(f)

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

# Sesja ONNX
session = ort.InferenceSession(f"{MODEL_DIR}/model.onnx")


def predict_intent(text):
    inputs = tokenizer(text, return_tensors="np")

    ort_inputs = {"input_ids": inputs["input_ids"], "attention_mask": inputs["attention_mask"]}

    outputs = session.run(None, ort_inputs)
    logits = outputs[0][0]

    probs = np.exp(logits) / np.sum(np.exp(logits))
    intent_id = int(np.argmax(probs))
    intent = LABELS[intent_id]

    return intent, probs


# TESTY
tests = [
    "stwórz folder testowy",
    "usuń plik log.txt",
    "odczytaj zawartość pliku dane.txt",
    "dopisz tekst do pliku",
    "wyświetl listę plików",
    "zainstaluj aktualizacje",
    "zapisz log systemowy",
]

for t in tests:
    intent, probs = predict_intent(t)
    print(f"Tekst: {t}")
    print(f"INTENCJA: {intent}")
    print(f"Prawdopodobieństwa: {probs}")
    print("-" * 40)
