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
    bigram = NgramService.generate(text=text, n=2)
    trigram = NgramService.generate(text=text, n=3)
    print("Bigram: ", bigram)
    print("Trigram: ", trigram)
