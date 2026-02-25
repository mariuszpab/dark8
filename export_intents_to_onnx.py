import os

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_DIR = r"C:\DARK8_MARK01\dark8_mark01\nlp\models\intent_trained"
ONNX_PATH = r"C:\DARK8_MARK01\dark8_mark01\nlp\models\intent_trained\intent_classifier.onnx"

os.makedirs(os.path.dirname(ONNX_PATH), exist_ok=True)

print("Ładuję tokenizer i model z wytrenowanego katalogu...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

dummy_text = "testowe zdanie dla eksportu"
inputs = tokenizer(
    dummy_text,
    return_tensors="pt",
    padding="max_length",
    truncation=True,
    max_length=64,
)

input_names = ["input_ids", "attention_mask"]
output_names = ["logits"]

print("Eksportuję do ONNX...")
torch.onnx.export(
    model,
    (inputs["input_ids"], inputs["attention_mask"]),
    ONNX_PATH,
    input_names=input_names,
    output_names=output_names,
    dynamic_axes={
        "input_ids": {0: "batch_size"},
        "attention_mask": {0: "batch_size"},
        "logits": {0: "batch_size"},
    },
    opset_version=13,
)

print(f"Zapisano model ONNX do: {ONNX_PATH}")
