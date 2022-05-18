import re

from nltk import word_tokenize, pos_tag  # 分词、词性标注
from nltk.corpus import stopwords  # 停用词
from nltk.stem import WordNetLemmatizer  # 词性还原
from util import mysql as mysql
from nltk import FreqDist
import matplotlib.pyplot as plt
from string import punctuation



# stoplist construction
def stopWordsListConstruction():
    videos_all = mysql.selectWordToken()
    videos = ' '.join(videos_all)
    cutwords = word_tokenize(videos)
    wordcount = {}
    for word in cutwords:
        wordcount[word] = wordcount.get(word, 0)+1
    minimum_token=sorted(wordcount.items(), key=lambda x: x[1], reverse=True)

    print('the minimum token occurrence: ',minimum_token)

    path='output files/txt files/stop words which less than 3 occurrences.txt'
    with open(path, 'w', encoding='utf-8') as file:
        for item in minimum_token:
            if item[1]<3:
                file.write(item[0]+',')


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
    plt.savefig('output files/line charts/Most Frequent words in corpus.jpg')
    plt.show()



def nltkUsing(paragraph):
    stoplist = [ 'get', 'go', 'im', 'like', 'one', 'oh', 'right', 'thats', 'really', 'yeah']
    lines= open('output files/txt files/stop words which less than 3 occurrences.txt','r',encoding='utf-8')
    for line in lines:
        list_minocc=eval(line)
    stoplist.extend(list_minocc)

    paragraph = paragraph.lower()

    # print('【remove punctuation：】')
    for pun in punctuation:
        paragraph = paragraph.replace(pun,'')

    cutwords = word_tokenize(paragraph)

    # print(cutwords)
    original_word = len(cutwords)

    # print('\nremove stop words in stoplist')
    # keep not or no
    stops =[stopword for stopword in stopwords.words('english') if stopword not in ['not', 'no']]
    cutwords1 = [word for word in cutwords if word not in stops]

    # print('\nremove stop words in our stoplist')

    cutwords1 = [word for word in cutwords1 if word not in stoplist]

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
    videoIds = mysql.SelectVideoID()
    print(len(videoIds))
    for i in range(len(videoIds)):
        videoId = videoIds[i]
        transcript = mysql.SelectVideos(videoId)
        transcript_new, original_word, new_word = nltkUsing(transcript)

        mysql.insertNewTranscript(videoId, transcript_new, original_word, new_word)

        if i%100==1:
            print('We have achieving ', i + 1, ' videos.')

    comments, id_list = mysql.SelectAllComments()
    print(len(comments))
    for index in range(len(comments)):
        id = id_list[index]
        comment=comments[index]
        # print(id)
        comment_new, original_word, new_word = nltkUsing(comment)
        mysql.insertNewComments(id, comment_new, original_word, new_word)
        if index%1000==1:
            print('We have achieving ', index + 1, ' comments.')

