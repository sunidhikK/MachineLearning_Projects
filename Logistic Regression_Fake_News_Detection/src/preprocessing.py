

import re
import string


def clean_text(text) -> str:
   

    if text is None:
        return ""

    text = str(text)

    if text.strip().lower() == "nan":
        return ""

    text = text.lower()

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove numbers
    text = re.sub(r"\d+", " ", text)

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Collapse extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


if __name__ == "__main__":
    sample = """
    Trump won the election in 2024!!
    Read more at https://abc.com or email us at tips@news.com
    """

    print("Original Text:\n", sample)
    print("\nCleaned Text:\n", clean_text(sample))
