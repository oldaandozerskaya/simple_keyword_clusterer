import re
import nltk
from nltk.corpus import stopwords

import pkgutil
import pymorphy2, re
ma = pymorphy2.MorphAnalyzer()


STOPWORDS = list(set(stopwords.words("russian")))

to_remove = pkgutil.get_data(__package__, 'blacklist.txt').decode('utf8').splitlines()

STOPWORDS.extend(to_remove)

KEYWORDS_TO_NORMALIZE = pkgutil.get_data(__package__, 'to_normalize.txt').decode('utf8').splitlines()
KEYWORDS_TO_NORMALIZE = [eval(x) for x in KEYWORDS_TO_NORMALIZE]

def sanitize_text(text: str, remove_stopwords: bool) -> str:
    """This utility function sanitizes a string by:
    - removing links
    - removing special characters
    - removing numbers
    - removing stopwords
    - transforming in lowercase
    - removing excessive whitespaces

    Args:
        text (str): the input text you want to clean
        language (str): the language used to remove stopwords
        remove_stopwords (bool): whether or not to remove stopwords

    Returns:
        str: the cleaned text
    """

    # remove links
    text = re.sub(r"http\S+", "", text)
    # remove special chars and numbers
    text = re.sub("[^А-Яа-я]+", " ", text)
    # remove stopwords
    if remove_stopwords:
        # 1. tokenize
        tokens = nltk.word_tokenize(text)
        # 2. check if stopword
        tokens = [w for w in tokens if not w.lower() in STOPWORDS]
        # 3. join back together
        text = " ".join(tokens)
    #terms_normalized = []
    #for term in term_extractor(text):
        #terms_normalized.append(term.normalized.replace(' ','_'))
    #text = ' '.join(terms_normalized)
    text = " ".join(ma.parse(word)[0].normal_form for word in text.split())
    #new_text = []
    #for word in text.split():
      #if len(word)>3 and (ma.parse(word)[0].tag.POS == 'NOUN' or ma.parse(word)[0].tag.POS == 'INFN'):
        #new_text.append(word)
    #text = ' '.join(new_text)
    # return text in lower case and stripped of whitespaces
    text = text.lower().strip()
    return text


def normalize_role(text):
    for wrong, right in KEYWORDS_TO_NORMALIZE:
        if wrong in text:
            return right + " " + text[len(wrong) + 1 :]
        else:
            return text
