import re
from dataclasses import dataclass
from nltk.tokenize import word_tokenize

_URI_PATTERN = r"<http.*>"
_URI_COMPILED = re.compile(_URI_PATTERN)


@dataclass
class RdfData:
    text: str

    def __call__(self):
        text_lines = self.text.split(".\n")
        text_only = [re.sub(_URI_PATTERN, "", text_line).strip() for text_line in text_lines]
        return text_only

    def get_uri(self, idx):
        required_text = self.text.split(".\n")[idx]
        uri, title = _URI_COMPILED.search(required_text).group().split(" ")
        return uri


def get_indexes(rdf_data, keyword, phrase_search=False):
    keyword_indexes = []
    keyword_positions = {}
    if phrase_search:
        first_word, second_word = keyword.split()
        first_word_pattern = f"{re.escape(first_word)}"
        second_word_pattern = f"{re.escape(second_word)}"
    for index_counter, line in enumerate(rdf_data):
        #  https: // stackoverflow.com / questions / 10196462 / regex - word - boundary - excluding - the - hyphen
        pattern = f"{re.escape(keyword)}\\b(?![\w-])"
        # print(pattern)
        #         if keyword in line:
        search_pattern = re.search(pattern, line, re.IGNORECASE)
        if search_pattern:
            keyword_indexes.append(index_counter)
            if not phrase_search:
                continue
        if phrase_search and search_pattern:
            # nltk_words = word_tokenize(line)
            # clean_text = line
            clean_text = re.sub(r'(\d+\.\d+\-)', 'unk', line)
            # clean_text = re.sub(r"/\w*/", "cmp cmp cmp", clean_text)
            # clean_text = clean_text.replace(".", " ").replace("'", " ").replace("-", "").replace(",", "")
            # clean_text = re.sub(r'[^\w\s]', '', clean_text)
            # clean_text = re.sub(r'[\\\*\"\'\(\)]', '', clean_text)
            # text_list = clean_text.split()
            text_list = re.findall(r'\b\w+\b', clean_text)
            positions = []
            previous_word = ""
            for index, word in enumerate(text_list):
                if re.search(first_word_pattern, previous_word, re.IGNORECASE) and re.search(second_word_pattern, word, re.IGNORECASE):
                    positions.append(index)
                previous_word = word
            # keyword_positions[index_counter] = text_list.index(keyword) + 1
            if positions and search_pattern:
                # print(text_list)
                keyword_positions[index_counter] = positions
    if not phrase_search:
        return keyword_indexes

    return keyword_indexes, keyword_positions


def get_search_results(rdf_data, conjuction, query, phrase_search=False):
    if not phrase_search:
        keyword_results = {}
        for keyword in query.split(conjuction):
            clean_keyword = keyword.strip()
            keyword_results[clean_keyword] = get_indexes(rdf_data, clean_keyword)
        value1, value2 = list(keyword_results.values())
        if conjuction == "OR":
            return set(value1).union(set(value2))
        if conjuction == "AND":
            return set(value1).intersection(set(value2))
        return set(value1).difference(set(value2))
    _, keyword_positions = get_indexes(rdf_data, query, phrase_search=True)
    return keyword_positions


def conjuction_index(conjuctions, query):
    for index, conjuction in enumerate(conjuctions):
        if conjuction in query:
            return index
    return "None"