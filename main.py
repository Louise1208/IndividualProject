import re

import nltk
from data_collection import data_collecting as dcol
from topic_modelling import data_preprocessing as dp
from data_clean import data_cleaning as dcl
from topic_modelling import find_best_parameters_lda as lda
from topic_modelling import optimist_LDA_model as bestLda
from util import mysql as mysql
from sentiment_analysis import sentiment_analysing as sa

if __name__ == '__main__':
    # if we need to download some tool in nltk
    # nltk.download()

    # Do data Collection: go to data_collection/data_collecting

    # Clean data:
    dcl.dataCleaning()

    # Do Data Pre-processing:
    # constrict stop words list:
    dp.stopWordsListConstruction()
    # Do Data Pre-processing with nltk
    dp.dataPreprocessing()



    # lda.LDAvis()

    # Topic Modelling
    lda.findBestParameters()
    lda.LDAvis()
    bestLda.topics()
    bestLda.findDocsTopics('videos')
    bestLda.findDocsTopics('comments')


    # Sentiment Analysis
    sa.sentimentAnalysis('videos')
    sa.sentimentAnalysis('comments')
    sa.evaluationSentiment()

    # close mysql cur
    mysql.CloseAll()
