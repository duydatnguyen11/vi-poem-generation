from loguru import logger
from poem_gpt_neo_model import model, tokenizer
from transformers import pipeline


def generating_poem(prompt: str):
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

    results = generator(
        prompt,
        max_new_tokens=250,  # The maximum number of tokens that can be generated (default: 50)
        do_sample=True,  # Whether to sample the next token or use beam search (default: False)
        top_k=50,  # The number of highest probability vocabulary tokens to keep for sampling (default: 50)
        top_p=0.95,  # The cumulative probability of sampling only from the top_k tokens (default: 1.0)
        temperature=1,  # Controls the randomness of the generated text (default: 1.0)
        repetition_penalty=1.2,  # Penalty to be applied to sequences to reduce repetition (default: 1.0)
    )

    generated_poem = results[0]["generated_text"]
    logger.info("Poem is generated successfully!")
    poem_lines = generated_poem.split("\n")

    # Print the generated poem line by line
    logger.info("Generated Poetry:")
    for line in poem_lines:
        print(line.strip())  # Strip whitespace from each line

    return poem_lines


if __name__ == "__main__":
    generating_poem("Tại sao ta lại khóc")
