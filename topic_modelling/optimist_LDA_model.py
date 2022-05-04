# 输入模型，训练好的dictionary和新的分词好的文档docs
# 查看docs里包含了哪些文档
import matplotlib.pyplot as plt

import util.mysql as mysql

from time import time
from gensim import corpora, models


def buildCorpus():
    t0 = time()
    results = mysql.selectWordToken()
    print('Get data samples :', len(results))
    # 创建语料的词语词典，每个单独的词语都会被赋予一个索引
    data_sample = [doc.split() for doc in results]
    # print(data_sample[0])
    dictionary = corpora.Dictionary(data_sample)

    # 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵(corpus)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in data_sample]
    print("Get corpus，cost time:  %0.3f s." % (time() - t0))
    return doc_term_matrix, dictionary, data_sample


def bestLDAmodel():
    model = models.LdaModel
    # TODO: fname best situation?
    lda = model.load('.model')
    return lda


# Show topics
def topics():
    lda = bestLDAmodel()
    topics = lda.print_topics(num_words=20)
    # 输出结果
    for topic in topics:
        print(topic)


# find the Topics of docs and the details of docs
def findDocsTopics():
    # todo
    lda = bestLDAmodel()
    videoIds = mysql.SelectVideoID()
    for videoId in videoIds:
        comments, id_list = mysql.SelectCommentswithID(videoId)
        docs = [doc.split() for doc in comments]
        dictionary = lda.id2word.doc2bow(docs)
        document_topics, word_topic, word_phi = lda.get_document_topics(dictionary, per_word_topics=True)
        if len(document_topics) == len(comments):
            if len(document_topics) == len(id_list):
                print('correct!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('comment:', comments[0], '\ndocument topics:', document_topics[0], '\nword topics:', word_topic[0],
              '\nword phi:', word_phi[0])
        print(document_topics)
        for doc_topic in document_topics:
            index = document_topics.index[doc_topic]
            id = id_list[index]
            print(id)
            print(comments[index])
            print('document topic:', doc_topic)
            print(doc_topic[0])
            topic = doc_topic[0][0]
            print(topic)
            print('-------------- \n')
            # mysql.insertTopicComment(id,videoId,topic)

# per_word_topics-将其设置为True可以提取给定单词的最有可能的主题。设置培训过程的方式是将每个单词分配给一个主题。否则，将省略没有指示性的词。 phi_value是引导此过程的另一个参数-它是一个单词的阈值，该单词是否被视为指示性单词。
