from wikisearch.deps.zhtools.zh_wiki import *
from wikisearch.deps.zhtools.langconv import *


def Traditional2Simplified(sentence):
    """transform traditional chinese characters into simplified chinese characters

    Args:
        sentence (str): a string of chineses characters

    Returns:
        sentence (str): simplified string
    """
    sentence = Converter('zh-hans').convert(sentence)
    return sentence