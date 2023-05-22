import re
import sys

from sudachipy import Dictionary, SplitMode


class MorphologicalAnalysisService:
    @classmethod
    def generate(cls, text: str) -> list[str]:
        preprocessed_text = cls._cleansing(text=text)
        sudachi = Dictionary().create()
        morphemes = [
            m.surface()
            for m in sudachi.tokenize(text=preprocessed_text, mode=SplitMode.C)
        ]
        return morphemes

    @classmethod
    def _cleansing(cls, text: str) -> str:
        preprocessed_text = re.sub(pattern=r"[^\w]", repl="", string=text)
        return preprocessed_text


if __name__ == "__main__":
    text = sys.argv[1]
    morphemes = MorphologicalAnalysisService.generate(text=text)
    print(morphemes)
