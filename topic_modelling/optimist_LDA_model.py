import util.mysql as mysql
from gensim import models

def bestLDAmodel():
    model = models.LdaModel
    lda = model.load('p10_c512_lda_model_numT7.model')
    return lda


# Show topics
def topics():
    lda = bestLDAmodel()
    topics = lda.print_topics(num_words=10)
    # 输出结果
    for topic in topics:
        print(topic)


# find the Topics of docs and the details of docs
def findDocsTopics(tag):
    lda = bestLDAmodel()
    docs=[]
    id_list=[]

    if tag=='comments':
        # get comments topics
        comments, id_list = mysql.SelectAllComments()
        docs = [doc.split() for doc in comments]
    if tag=='videos':
        # get transcripts topics:
        transcripts = []
        id_list = mysql.SelectVideoID()
        for videoId in id_list:
            videosContent = mysql.SelectVideos(videoId)
            transcripts.append(videosContent)
        docs = [doc.split() for doc in transcripts]

    print(tag,len(docs))

    for index in range(len(docs)):
        doc = docs[index]
        doc_bow = lda.id2word.doc2bow(doc)
        document_topics = lda.get_document_topics(doc_bow)
        document_topics = sorted(document_topics, key=lambda k: k[1], reverse=True)

        # print('\ndocument topics:', document_topics)
        possibilities=[]
        topics=[]
        for i in range(len(document_topics)):
            possi = round(document_topics[i][1], 4)
            possibilities.append(possi)
            topics.append(document_topics[i][0])

        topic=[topics[0]]
        possibility=[possibilities[0]]
        # print(possibilities)
        for i in range(len(possibilities)-1):
            if possibilities[i]-possibilities[i+1]<0.05:
                topic.append(str(topics[i+1]))
                possibility.append(str(possibilities[i+1]))
            else:
                # print(topic)
                break

        # print(tag,index,': ',topic,possibility)

        if tag=='comments':
            id = id_list[index]
            # print('id: ',id)
            mysql.insertTopicComment(id, str(topic), str(possibility))

        if tag=='videos':
            videoId = id_list[index]
            # print('videoId: ',videoId)
            mysql.insertTopicTranscript(videoId, str(topic), str(possibility))


        if index % 1000 == 1:
            print(index)

    print(tag,' get topics!')
