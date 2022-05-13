from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from util import mysql as mysql

from sklearn.metrics import confusion_matrix
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


    if tag=='videos':
        print(tag,': start to analyse...')
        id_list=mysql.SelectVideoID()

        for videoId in id_list:
            content=mysql.selectTranscripts(videoId)
            contents.append(content)

    for index in range(len(contents)):
        id = id_list[index]
        content=contents[index]

        # calculate the number of sentences
        sentence_c = sent_tokenize(content)
        num_sentence = num_sentence + len(sentence_c)

        # sentiment analysis
        result = analyzer.polarity_scores(content)
        # print(id,': ', result)
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
            mysql.InsertCommentsSAResult(id, compound, sentiment)
            if temp%1000==1:
                print(tag,temp, 'collect!')
        if tag=='videos':
            mysql.InsertVideosSAResult(id, compound, sentiment)
            if temp%100==1:
                print(tag,temp, 'collect!')
        temp = temp + 1
    print('number of sentences:', num_sentence)
    print('all sentimnent collect!!!!!!!!!!')
    # save the number of sentences of input tag
    with open('output files/txt files/number of sentences.txt', 'a', encoding='utf-8') as file:
        file.write('num_sentence of ' +str(tag)+'  = '+ str(num_sentence)+'\n')

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

    print(classification_report(actual, vader_sentiment))
    path = 'output files/txt files/evaluation of sentiment analysis.txt'
    with open(path, 'a', encoding='utf-8') as file:
        file.write('confusion_matrix:')
        file.write(str(confusion_m))
        file.write('\n\n')
        file.write(classification_report(actual, vader_sentiment))
