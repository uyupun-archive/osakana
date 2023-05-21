def generate_ngrams(text: str, n: int) -> list[str]:
    words = text.split(" ")
    ngrams = []
    for word in words:
        for i in range(len(word) - n + 1):
            ngrams.append(word[i:i+n])
    return ngrams

title = "蒋介石(しょうかいせき)とは？ 意味や使い方 - コトバンク"
print(generate_ngrams(text=title, n=2))
print(generate_ngrams(text=title, n=3))
