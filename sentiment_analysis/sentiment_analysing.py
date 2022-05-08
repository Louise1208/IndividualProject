import random
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from util import mysql as mysql

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import classification_report


def sentimentAnalysis(tag):

    analyzer = SentimentIntensityAnalyzer()
    temp = 0
    num_sentence = 0
    id_list=[]
    contents=[]
    if tag=='comments':
        print(tag,': start to analyse...')
        contents, id_list = mysql.SelectAllComments()
        analyzer = SentimentIntensityAnalyzer()


    if tag=='videos':
        print(tag,': start to analyse...')
        id_list=mysql.SelectVideoID()
        for videoId in id_list:
            content=mysql.SelectVideos(videoId)
            contents.append(content)

    for index in range(len(contents)):
        id = id_list[index]
        content=contents[index]

        result = analyzer.polarity_scores(content)
        sentence_c = sent_tokenize(content)
        num_sentence = num_sentence + len(sentence_c)
        # print(num_sentence)
        neg = str(result['neg'])
        neu = str(result['neu'])
        pos = str(result['pos'])
        compound = result['compound']  # neg<-0.05<neu<0.05<pos
        if compound <= -0.05:
            sentiment = -1
        elif compound >= 0.05:
            sentiment = 1
        else:
            sentiment = 0
        compound = str(compound)
        # print(compound)
        if tag=='comments':
            mysql.InsertCommentsSAResult(id, neg, neu, pos, compound, sentiment)
            if temp%1000==1:
                print(temp, 'collect!')
        if tag=='videos':
            mysql.InsertVideosSAResult(id, neg, neu, pos, compound, sentiment)
            if temp%100==1:
                print(temp, 'collect!')
        temp = temp + 1
    print('number of sentences:', num_sentence)
    print('all sentimnent collect!!!!!!!!!!')
    with open('number of sentences.txt', 'a', encoding='utf-8') as file:
        file.write('num_sentence=' + str(num_sentence))



def evaluationSentiment():
    # select actual and bader results from mysql
    actual = mysql.selectActuralSentiment()
    vader_sentiment = mysql.selectResultsSentiment()
    print('actual:', actual)
    print('vader_sentiment:', vader_sentiment)
    print(classification_report(actual, vader_sentiment))

    # confusion matrix
    confusion_m = confusion_matrix(actual, vader_sentiment)  # 横为true 竖为predict
    print('confusion_m: \n', confusion_m)

    # accuracy
    accuracy = accuracy_score(actual, vader_sentiment)
    print('accuracy: ', accuracy)
    # precision_score
    precision_micro = precision_score(actual, vader_sentiment, average='micro')  # 微平均
    precision_macro = precision_score(actual, vader_sentiment, average='macro')  # 宏平均
    precision_weighted = precision_score(actual, vader_sentiment, average='weighted')  # 加权平均
    print('precision_micro: ', precision_micro, '\nprecision_macro:', precision_macro, '\nprecision_weighted: ',
          precision_weighted)

    # Recall
    recall_micro = recall_score(actual, vader_sentiment, average='micro')
    recall_macro = recall_score(actual, vader_sentiment, average='macro')
    recall_weighted = recall_score(actual, vader_sentiment, average='weighted')
    print('recall_micro: ', recall_micro, '\nrecall_macro:', recall_macro, '\nrecall_weighted: ', recall_weighted)

    # F1 score
    F1_micro = f1_score(actual, vader_sentiment, average='micro')
    F1_macro = f1_score(actual, vader_sentiment, average='macro')
    F1_weighted = f1_score(actual, vader_sentiment, average='weighted')
    print('F1_micro: ', F1_micro, '\nF1_macro:', F1_macro, '\nF1_weighted: ', F1_weighted)

    path = 'output files/txt files/evaluation of sentiment analysis.txt'
    with open(path, 'a', encoding='utf-8') as file:
        file.write('confusion_matrix:')
        file.write(str(confusion_m))
        file.write('\n\n')
        file.write('accuracy: ' + str(accuracy) + '\n')
        file.write('precision_micro: ' + str(precision_micro) + '\nprecision_macro:' + str(
            precision_macro) + '\nprecision_weighted: ' + str(precision_weighted) + '\n\n')
        file.write(
            'recall_micro: ' + str(recall_micro) + '\nrecall_macro:' + str(recall_macro) + '\nrecall_weighted: ' + str(
                recall_weighted) + '\n\n')
        file.write('F1_micro: ' + str(F1_micro) + '\nF1_macro:' + str(F1_macro) + '\nF1_weighted: ' + str(
            F1_weighted) + '\n\n')
        file.write(classification_report(actual, vader_sentiment))
