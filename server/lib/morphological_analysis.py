import re
import sys

from sudachipy import Dictionary, MorphemeList, SplitMode


class MorphologicalAnalysisService:
    @classmethod
    def generate(cls, text: str) -> list[str]:
        preprocessed_text = cls._cleansing(text=text)
        sudachi = Dictionary().create()
        morphemes = sudachi.tokenize(text=preprocessed_text, mode=SplitMode.C)
        filtered_morphemes = cls._filter_morphemes(morphemes=morphemes)
        return filtered_morphemes

    @classmethod
    def _filter_morphemes(cls, morphemes: MorphemeList) -> list[str]:
        filtered_morphemes = []
        for morpheme in morphemes:
            pos = morpheme.part_of_speech()[0]
            if pos not in ["助詞", "助動詞"]:
                filtered_morphemes.append(morpheme.surface())
        return filtered_morphemes

    @classmethod
    def _cleansing(cls, text: str) -> str:
        preprocessed_text = re.sub(pattern=r"[^\w]", repl="", string=text)
        return preprocessed_text


if __name__ == "__main__":
    text = sys.argv[1]
    morphemes = MorphologicalAnalysisService.generate(text=text)
    print(morphemes)
