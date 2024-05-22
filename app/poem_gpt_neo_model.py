from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "duydatnguyen/vi-poem-gpt-neo"


def downloading_model(model_path):

    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    logger.info("Downloading successfully")
    return tokenizer, model


tokenizer, model = downloading_model(MODEL_ID)
