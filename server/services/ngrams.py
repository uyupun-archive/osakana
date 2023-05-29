import re
import sys


class NgramService:
    @classmethod
    def generate(cls, text: str, n: int) -> list[str]:
        preprocessed_text = cls._cleansing(text=text)
        words = preprocessed_text.split(" ")
        ngrams = []
        for word in words:
            for i in range(len(word) - n + 1):
                ngrams.append(word[i : i + n])
        return ngrams

    @classmethod
    def _cleansing(cls, text: str) -> str:
        preprocessed_text = re.sub(pattern=r"[^\w\s]", repl="", string=text)
        return preprocessed_text


if __name__ == "__main__":
    text = sys.argv[1]
    bigrams = NgramService.generate(text=text, n=2)
    trigrams = NgramService.generate(text=text, n=3)
    print("Bigrams: ", bigrams)
    print("Trigrams: ", trigrams)
