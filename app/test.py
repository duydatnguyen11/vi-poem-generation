from loguru import logger
from pipeline import generating_poem


def test_generating_poem():
    prompt = "Những nẻo đường ta đã đi qua"
    poem_lines = generating_poem(prompt)
    logger.info("Generated Poetry: {}", poem_lines)
    # Check if the function returns a list
    assert isinstance(poem_lines, list), "The output should be a list of lines."

    # Check if the list is not empty
    assert len(poem_lines) > 0, "The list of poem lines should not be empty."

    # Check if each element in the list is a string
    for line in poem_lines:
        assert isinstance(line, str), "Each line should be a string."


if __name__ == "__main__":
    test_generating_poem()
    print("All tests passed!")
