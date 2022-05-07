import util.mysql as mysql
from gensim import models
import pandas as pd

def bestLDAmodel():
    model = models.LdaModel
    lda = model.load('p20_c1024_lda_model_numT5.model')
    return lda


# Show topics
def topics():
    lda = bestLDAmodel()
    topics = lda.print_topics(num_words=10)
    # 输出结果
    for topic in topics:
        print(topic)


# find the Topics of docs and the details of docs
def findDocsTopics():
    # todo
    lda = bestLDAmodel()

    # get comments topics
    comments, id_list = mysql.SelectAllComments()
    docs = [doc.split() for doc in comments]
    for doc in docs:
        index=docs.index(doc)

        doc_bow= lda.id2word.doc2bow(doc)
        document_topics= lda.get_document_topics(doc_bow)
        document_topics=sorted(document_topics,key=lambda k:k[1],reverse=True)
        # print('\ndocument topics:', document_topics)
        topic=document_topics[0][0]
        possibility=document_topics[0][1]
        possibility=round(possibility,4)
        id=id_list[index]
        # print(id)
        mysql.insertTopicComment(id,topic,str(possibility))
    print('all comments tag!')

    # get transcripts topics:
    transcripts=[]
    videoIds=mysql.SelectVideoID()
    print(len(videoIds))
    for videoId in videoIds:
        videosContent=mysql.SelectVideos(videoId)
        transcripts.append(videosContent)
    docs = [doc.split() for doc in transcripts]
    uncertain_docs=[]
    for doc in docs:
        index=docs.index(doc)
        videoId=videoIds[index]
        doc_bow= lda.id2word.doc2bow(doc)
        document_topics= lda.get_document_topics(doc_bow)
        document_topics=sorted(document_topics,key=lambda k:k[1],reverse=True)
        # print(document_topics)

        topic=document_topics[0][0]
        possibility=document_topics[0][1]
        possibility=round(possibility,4)

        mysql.insertTopicTranscript(videoId,topic,str(possibility))

        if (possibility-round(document_topics[1][1],4))<0.1:
                uncertain_docs.append([videoId,document_topics])
                print(videoId,': ',document_topics)

        path = 'output files/txt files/uncertain_transcripts.txt'
        with open(path, 'w', encoding='utf-8') as file:
            for doc in uncertain_docs:
                file.write(str(doc)+'\n')
    print('all videos topic collect!')



