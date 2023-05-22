import sys


class NgramService:
    @classmethod
    def generate(cls, text: str, n: int) -> list[str]:
        words = text.split(" ")
        ngrams = []
        for word in words:
            for i in range(len(word) - n + 1):
                ngrams.append(word[i:i+n])
        return ngrams


if __name__ == "__main__":
    text = sys.argv[1]
    bigrams = NgramService.generate(text=text, n=2)
    trigrams = NgramService.generate(text=text, n=3)
    print("Bigrams: ", bigrams)
    print("Trigrams: ", trigrams)
