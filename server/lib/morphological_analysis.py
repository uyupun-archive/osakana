import sys

from sudachipy import Dictionary, SplitMode


class MorphologicalAnalysisService:
    @classmethod
    def generate(cls, text: str) -> list[str]:
        sudachi = Dictionary().create()
        morphemes = [m.surface() for m in sudachi.tokenize(text, mode=SplitMode.C)]
        return morphemes


if __name__ == "__main__":
    text = sys.argv[1]
    morphemes = MorphologicalAnalysisService.generate(text=text)
    print(morphemes)
