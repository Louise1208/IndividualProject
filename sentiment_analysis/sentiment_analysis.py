import random
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from textblob import TextBlob
from tools import mySQL as mysql

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import classification_report


def sentimentAnalysis():
    comments,id_list= mysql.SelectAllComments()
    analyzer=SentimentIntensityAnalyzer()
    temp=0
    num_sentence=0
    for comment in comments:
            index=comments.index(comment)
            id=id_list[index]
            result=analyzer.polarity_scores(comment)
            sentence_c=sent_tokenize(comment)
            num_sentence=num_sentence+len(sentence_c)
            # print(num_sentence)
            neg=str(result['neg'])
            neu=str(result['neu'])
            pos=str(result['pos'])
            compound=result['compound']  # neg<-0.05<neu<0.05<pos
            if compound<=-0.05:
                sentiment=-1
            elif compound >=0.05:
                sentiment=1
            else:
                sentiment=0
            compound=str(compound)
            # print(compound)
            mysql.InsertCommentsSAResult(id,neg, neu,pos,compound,sentiment)
            print(temp,' total commnets: 39374')
            temp=temp+1
    print('number of sentences:',num_sentence)
    print('all sentimnent collect!!!!!!!!!!')
    with open('number of sentences.txt', 'a', encoding='utf-8') as file:
        file.write('num_sentence='+str(num_sentence))


# 结束啦
def sentimentAnalysisTrain():
    comments,id_list = mysql.SelectAllComments()
    print(id_list)
    test_number=int(len(id_list)*0.2)
    id_test=random.sample(id_list, test_number)
    print(len(id_test))
    temp=0
    for id in id_test:
        index=id_list.index(id)
        comment=comments[index]
        comment = comment.lower()
        comment = TextBlob(comment)
        comment = str(comment.correct())
        comment_blob = TextBlob(comment)
        polarity = comment_blob.sentiment.polarity
        subjectivity = comment_blob.sentiment.subjectivity
        # print(polarity, subjectivity)
        if polarity>= 0.1:
                polarity=1
        elif polarity <= -0.1:
            polarity=-1
        else:
            polarity=0
        if subjectivity ==0:
             subjectivity='obj'
             polarity=0


        mysql.InsertCommentsTestSA(id, polarity, subjectivity)
        print(temp,'total comments: 39374')
        temp=temp+1


def evaluationSentiment():
    # TODO
    # accurancy.
    actural=mysql.selectActuralSentiment()
    vader_sentiment=mysql.selectResultsSentiment()
    print('actural:',actural)
    print('vader_sentiment:',vader_sentiment)

    # confusion matrix
    confusion_m=confusion_matrix(actural,vader_sentiment)  #横为true 竖为predict
    print('confusion_m: ',confusion_m)

    # accuracy
    accuracy=accuracy_score(actural,vader_sentiment)
    print('accuracy: ',accuracy)
    #precision_score
    precision_micro=precision_score(actural,vader_sentiment,average='micro') #微平均
    precision_macro=precision_score(actural,vader_sentiment,average='macro') #宏平均
    precision_weighted=precision_score(actural,vader_sentiment,average='weighted') #加权平均
    print('precision_micro: ',precision_micro,'\nprecision_macro:',precision_macro,'\nprecision_weighted: ',precision_weighted)

    # Recall
    recall_micro=recall_score(actural,vader_sentiment,average='micro')
    recall_macro=recall_score(actural,vader_sentiment,average='macro')
    recall_weighted=recall_score(actural,vader_sentiment,average='weighted')
    print('recall_micro: ',recall_micro,'\nrecall_macro:',recall_macro,'\nrecall_weighted: ',recall_weighted)

    # F1 score
    F1_micro=f1_score(actural,vader_sentiment,average='micro')
    F1_macro=f1_score(actural,vader_sentiment,average='macro')
    F1_weighted=f1_score(actural,vader_sentiment,average='weighted')
    print('F1_micro: ',F1_micro,'\nF1_macro:',F1_macro,'\nF1_weighted: ',F1_weighted)

    print(classification_report(actural,vader_sentiment))
    path='evaluation of sentiment analysis.txt'
    with open(path, 'a', encoding='utf-8') as file:
        file.write('confusion_matrix:')
        file.write(confusion_m)
        file.write('\n\n')
        file.write('accuracy: '+str(accuracy)+'\n')
        file.write('precision_micro: '+str(precision_micro)+'\nprecision_macro:'+str(precision_macro)+'\nprecision_weighted: '+str(precision_weighted)+'\n\n')
        file.write('recall_micro: '+str(recall_micro)+'\nrecall_macro:'+str(recall_macro)+'\nrecall_weighted: '+str(recall_weighted)+'\n\n')
        file.write('F1_micro: '+str(F1_micro)+'\nF1_macro:'+str(F1_macro)+'\nF1_weighted: '+str(F1_weighted)+'\n\n')
        file.write(classification_report(actural,vader_sentiment))


