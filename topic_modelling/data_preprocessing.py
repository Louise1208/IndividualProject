import re

import gensim
from nltk import word_tokenize, pos_tag  # 分词、词性标注
from nltk.corpus import stopwords  # 停用词
from nltk.stem import WordNetLemmatizer  # 词性还原
from util import mysql as mysql
from nltk import FreqDist
import matplotlib.pyplot as plt

remainder = ' Solution 1: normal way \n Solution 2: Adding Stopwords Lists'


# stoplist construction
def stopWordsListConstruction():
    videos_all = mysql.selectWordToken()
    videos = ' '.join(videos_all)
    cutwords = word_tokenize(videos)
    words_frequncy = FreqDist(cutwords)
    most_fre_words = words_frequncy.most_common(30)
    t = ""
    for key in most_fre_words:
        t += '\'' + key[0] + '\''
        t += ','
    # print(t)
    most_fre_words = words_frequncy.most_common(20)
    words = [item[0] for item in most_fre_words]
    count = [item[1] for item in most_fre_words]

    # line chart
    fig = plt.figure(figsize=(15, 5))
    plt.plot(words, count, marker="o")
    plt.xlim(0, 20)
    plt.title("Most Frequent words in corpus")
    plt.xlabel("words")
    plt.ylabel("Count")
    plt.savefig('Most Frequent words in corpus.jpg')
    plt.show()



def nltkUsing(paragraph, solutionID):
    # our stop word list
    stoplist = ['get', 'go', 'oh', 'like', 'one', 'right', 'okay', 'na', 'gon', 'yeah']

    paragraph = paragraph.lower()
    # print('【去除标点符号结果：】')
    paragraph = re.sub(r'([^\w\u4e00-\u9fff])+', ' ', paragraph)
    paragraph = re.sub('_', ' ', paragraph)
    # print(paragraph)
    # 分词
    cutwords = word_tokenize(paragraph)
    # print(cutwords)
    original_word = len(cutwords)

    # print('\nremove stop words in stoplist')
    stops = set(stopwords.words("english"))
    cutwords1 = [word for word in cutwords if word not in stops]

    # print('\nremove stop words in our stoplist')
    if solutionID == 2:
        cutwords1 = [word for word in cutwords1 if word not in stoplist]

        # print(words_pos[0])
        # print(words_pos[0][1])

    # print('\nPart-of-speech restoration：')
    cutwords2 = []
    pos_vb = set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])
    words_pos = pos_tag(cutwords1)
    for word, pos in words_pos:
        if pos in pos_vb:
            cutwords2.append(WordNetLemmatizer().lemmatize(word, pos='v'))
        else:
            cutwords2.append(WordNetLemmatizer().lemmatize(word))
    # print(cutwords2)

    new_word = len(cutwords2)
    # combine into one string
    words_wc = ' '.join(cutwords2)
    # print(words_wc)
    return words_wc, original_word, new_word


def dataPreprocessing():
    print(remainder)
    solutionID = input('input ID of Data Preprocessing Solution: ')
    solutionID = int(solutionID)
    videoIds = mysql.SelectVideoID()
    print(len(videoIds))
    videos_all = []
    for i in range(len(videoIds)):
        videoId = videoIds[i]
        transcript = mysql.SelectVideos(videoId)
        transcript_new, original_word, new_word = nltkUsing(transcript, solutionID)
        videos_all.append(transcript_new)
        mysql.insertNewTranscript(videoId, transcript_new, original_word, new_word)
        comments, id_list = mysql.SelectCommentswithID(videoId)
        # print(videoId)
        for index in range(len(comments)):
            id = id_list[index]
            comment=comments[index]
            # print(id)
            comment_new, original_word, new_word = nltkUsing(comment, solutionID)
            mysql.insertNewComments(videoId, id, comment_new, original_word, new_word)
            videos_all.append(comment_new)
        print('We have achieving ', i + 1, ' videos.')
    if solutionID == 1:
        stopWordsListConstruction()
