from sudachipy import Dictionary, SplitMode

sudachi = Dictionary().create()
text = "蒋介石(しょうかいせき)とは？ 意味や使い方 - コトバンク"

words = [m.surface() for m in sudachi.tokenize(text, mode=SplitMode.C)]
print(words)
