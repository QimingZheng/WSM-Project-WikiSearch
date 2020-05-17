from wikisearch.deps.zhtools.zh_wiki import *
from wikisearch.deps.zhtools.langconv import *
import jieba

def Traditional2Simplified(sentence):
    """transform traditional chinese characters into simplified chinese characters

    Args:
        sentence (str): a string of chineses characters

    Returns:
        sentence (str): simplified string
    """
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

def text_segmentation(text):
    """segment chinese sentences

    Args:
        text (str): a string of chinese characters

    Returns:
        text (list(str)): a list of strings each is a segmented part
    """
    # jieba.enable_paddle()
    text = jieba.cut(text)
    return text