from utils.file_parser import *
from utils.words_utils import *
from sentences_db.sentences_db import SentencesDB
from data_manager.auto_complete_data import AutoCompleteData


class Data:
    """
    'Data' holds the sentences trie and handle user requests.
    """
    def __init__(self, path):
        self.__sentences = SentencesDB()
        self.__path = path

    def insert_data(self):
        # get all lines from path's files and insert each line to 'self.__sentences' trie
        for line in get_all_lines(self.__path):
            self.insert_to_trie(line)

    def insert_to_trie(self, sentence_details):
        # get all line suffixes and insert each suffix to 'self.__sentences' trie
        for line in get_all_suffix(sentence_details["line"]):
            self.__sentences.insert(clean_sentence(line), sentence_details["path"], sentence_details["line_num"])

    def query(self, prefix, count, fix_type=None, location=None):
        # search for 'prefix' in 'self.__sentences' trie.
        res = []
        for source in self.__sentences.query(prefix):
            with open(source[0], "r") as data_file:
                line = data_file.readlines()[source[1]].strip()
                offset = clean_sentence(line).find(prefix)
                score = self.calculate_score(fix_type, len(prefix), location)
                res.append(AutoCompleteData(line, source[0].split("\\")[-1], offset, score))
            if len(res) == count:
                return sorted(res, key=lambda k: (k.get_score(), k.get_complete_sentence()))
        return sorted(res, key=lambda k: (k.get_score(), k.get_complete_sentence()))

    def get_best_k_completion(self, prefix: str, k: int = 5) -> list[AutoCompleteData]:
        # search for best k completions for 'prefix'
        res = []
        res += self.get_completion(prefix, k)
        if k - len(res):
            res += self.get_completion_with_replace(prefix, k - len(res))
        if k - len(res):
            res += self.get_completion_with_delete(prefix, k - len(res))
        if k - len(res):
            res += self.get_completion_with_add(prefix, k - len(res))
        return res

    def get_completion(self, prefix, count: int):
        # search for exact completion for 'prefix'
        return self.query(prefix, count)

    def get_completion_with_replace(self, prefix: str, count: int) -> list[AutoCompleteData]:
        # search for completion for prefix with replacing of one letter of 'prefix'
        res: list[AutoCompleteData] = []
        for sentence, location in all_replacements(prefix):
            if len(res) >= count:
                return res
            res += self.query(sentence, count, "replace", location)
        return res

    def get_completion_with_add(self, prefix, count) -> list[AutoCompleteData]:
        # search for completion for prefix with adding one letter to 'prefix'
        res: list[AutoCompleteData] = []
        for sentence, location in all_additions(prefix):
            if len(res) >= count:
                return res
            res += self.query(sentence, count, "add", location)
        return res

    def get_completion_with_delete(self, prefix: str, count: int) -> list[AutoCompleteData]:
        # search for completion for prefix with deletion of one letter of 'prefix'
        res: list[AutoCompleteData] = []
        for sentence, location in all_deletions(prefix):
            if len(res) >= count:
                return res
            res += self.query(sentence, count, "delete", location)
        return res

    @staticmethod
    def calculate_score(fix_type: str, prefix_len: int, fix_location: int) -> int:
        # calculate score of result by fix_type and fix_location
        score = prefix_len * 2
        if fix_type == "delete" or fix_type == "add":
            if fix_location < 4:
                score -= 10 - fix_location * 2
            else:
                score -= 2
        elif fix_type == "replace":
            if fix_location < 4:
                score -= 5 - fix_location
            else:
                score -= 1
        return score
