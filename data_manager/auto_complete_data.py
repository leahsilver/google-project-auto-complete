from dataclasses import dataclass


@dataclass
class AutoCompleteData:
    """
    AutoCompleteData is a result that will be returned
     as a continuation option to the inserted sentence
    """

    def __init__(self, completed_sentence, source_text, offset, score):
        self.__completed_sentence: str = completed_sentence
        self.__source_text: str = source_text
        self.__offset: int = offset
        self.__score: int = score

    def __str__(self):
        return "{} ({} {})".format(self.__completed_sentence, self.__source_text, self.__offset)

    def get_score(self):
        return self.__score

    def get_complete_sentence(self):
        return self.__completed_sentence
