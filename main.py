import re
import warnings

warnings.filterwarnings("ignore")

import numpy as np
from nltk import pos_tag, WordNetLemmatizer
import nltk
from data_collection import data_collecting as dcol
from topic_modelling import data_preprocessing as dp
from data_clean import data_cleaning as dcl
from data_clean import data_classification as dc
from topic_modelling import find_best_parameters_lda as lda
from topic_modelling import optimist_LDA_model as bestLda
from util import mysql as mysql
from sentiment_analysis import sentiment_analysing as sa
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # if we need to download some tool in nltk
    # nltk.download()

    # Do data Collection
    dcol.dataCollecting()

    # Do data_calssification
    # dc.dataClassificationWithTags()

    # Clean data:
    dcl.dataCleaning()

    comments, id_list = mysql.SelectAllComments()
    print(len(comments))
    for index in range(len(comments)):
        comment = comments[index]
        id = id_list[index]
        if len(comment.split()) < 30:
            print(comment)
            mysql.delCommentsLessThan30(id)

    # Do Data Pre-processing with nltk and find the best dataPreprocessing way:
    dp.dataPreprocessing(1)
    # dp.dataPreprocessing(2)

    # Topic Modelling
    # lda.findBestParameters()
    # lda.LDAvis()
    # bestLda.topics()
    # bestLda.findDocsTopics()

    # Sentiment Analysis
    sa.sentimentAnalysis('videos')
    sa.sentimentAnalysis('comments')
    # sa.evaluationSentiment()

    mysql.CloseAll()
