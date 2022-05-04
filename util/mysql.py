import re

import pymysql

# 云服务器上mysql数据库连接
con = pymysql.connect(host='121.199.58.129',
                      port=3306,
                      user='userout',  # mysql的登录账号admin
                      password='userout',  # mysql的登录密码pwd
                      db='youtube')  # mysql中要访问的数据表

cur = con.cursor()


# print('数据库链接成功')
# 创建游标

# Data Collection：
def SelectVideoID():
    # query = "SELECT `video_id` from comments where new_comment is NULL"
    query = "SELECT `video_id` from comments"
    cur.execute(query)
    # 读取数据
    videoId = cur.fetchall()
    # 打印数据
    videoIds = []
    for items in videoId:
        for item in items:
            videoIds.append(item)
    # print(videoIds)
    return videoIds
# 选择 transcripts没有的video_id
def SelectVideoIDforThanscripts():
    # print('try to select video id for transcripts')
    # 执行sql语句
    query = "select video_id from videos where video_id not in (select video_id from transcripts) "
    # query = 'select video_id from comments where video_id not in (select video_id from transcripts) order by likes desc'
    cur.execute(query)
    con.commit()
    # 读取数据
    videoId = cur.fetchall()
    # 打印数据
    videoIds = []
    for items in videoId:
        for item in items:
            videoIds.append(item)
    # print(len(videoIds))
    return videoIds


# 收集transcript
def InsertTranscriptInf(videoId, transcription):
    # 执行sql语句
    query = 'insert into transcripts(`video_id`,`transcript`) values(%s,%s) '
    param = (videoId, transcription)
    cur.execute(query, param)
    con.commit()
    # print(videoId + 'GB Video transcription collect!')


# 选择 Comments 中没有的video_id
def SelectVideoIDforComments():
    # print('try to select video id for transcripts')
    # 执行sql语句
    query1 = 'create table tem_comments (select DISTINCT video_id from comments)'
    cur.execute(query1)
    con.commit()
    videoIds = []

    query2 = "select video_id from videos where video_id not in (select video_id from tem_comments) and video_id not in (select video_id from videos_without_comments) "
    cur.execute(query2)
    con.commit()
    # print(len(videoIds))
    # 读取数据
    videoId = cur.fetchall()
    # 打印数据
    for items in videoId:
        for item in items:
            videoIds.append(item)
    # print(len(videoIds))

    # print(len(videoIds))
    query3 = 'DROP TABLE IF EXISTS tem_comments'
    cur.execute(query3)
    con.commit()
    # print('ok')
    return videoIds


# 将没有comments[like]>200的video_id 插入videos_without_comments中：
def insertVideoswithoutComments(videoId):
    # print('start')
    query = 'insert into videos_without_comments (`video_id`) value(%s)'
    param = (videoId)
    cur.execute(query, param)
    con.commit()
    # print('insert!!')


# 收集comments
def InsertComments(videoid,comment):
    # 执行sql语句
    query = 'insert into comments(`video_id`,`comment`) values(%s, %s)'
    param = (videoid,comment)
    cur.execute(query, param)
    con.commit()

# For Data Selection
# 选择videos的tags并进行第一次粗浅的topic modelling：
def selectTags(videoId):
    query = 'select `tags` from videos where video_id = %s '
    param = (videoId)
    cur.execute(query, param)
    con.commit()
    tags = cur.fetchall()
    for items in tags:
        # print(items)
        for item in items:
            return item


# 插入tags于videos中
def insertNewTags(videoId, newTags):
    query = 'update videos set `tags`= %s where video_id = %s '
    param = (newTags, videoId)
    cur.execute(query, param)
    con.commit()

# For word clean:

def selectTranscripts(videoId):
    query = 'SELECT `transcript` from videos where video_id =%s'
    param = (videoId)
    cur.execute(query, param)
    # 读取数据
    transcripts = cur.fetchall()
    # print(transcripts)
    con.commit()
    # 打印数据
    videosContents = []
    # videosContents = ''
    for items in transcripts:
        for item in items:
            videosContents.append(item)
        # print(item)
    transcript=','.join(videosContents)
    # print(transcript)
    return transcript


# # insert cleaned comments：
def updateCleanedCommentsToComments(videoId, id,comment):
    # 执行sql语句
    # print(videoId,id,comment)
    query = 'update comments set `comment` = %s where video_id= %s and id=%s'
    param = (comment, videoId,id)
    cur.execute(query, param)
    con.commit()
# insert cleaned transcripts
def updateCleanedTranscripts(videoID, transcript):
    query = 'update videos set `transcript` = %s where video_id= %s'
    param = (transcript, videoID)
    cur.execute(query, param)
    con.commit()
    return None

# For word cut:
# 选择videos中的全部内容：
def SelectVideos(videoId):
    query = 'SELECT `title`,`transcript` from videos where video_id =%s'
    param = (videoId)
    cur.execute(query, param)
    # 读取数据
    videos = cur.fetchall()
    con.commit()
    # 打印数据
    videosContents = []
    for items in videos:
        for item in items:
            videosContents.append(item)
    # print(videosContents)
    videosContent='.'.join(videosContents)
    return videosContent

# 将videos的分词结果保存在new_transcript中
def insertNewTranscript(videoId, transcript_new, original_word, new_word):
    query = 'update videos set new_transcript= %s where video_id = %s '
    param = (transcript_new, videoId)
    cur.execute(query, param)
    con.commit()
    query = 'update videos set original_word= %s where video_id = %s '
    param = (original_word, videoId)
    cur.execute(query, param)
    con.commit()
    query = 'update videos set new_word= %s where video_id = %s '
    param = (new_word, videoId)
    cur.execute(query, param)
    con.commit()

# 将comments的分词结果保存在new_comment中
def insertNewComments(videoId,id, new_comment, original_word, new_word):
    query = 'update comments set new_comment= %s where video_id = %s and id=%s'
    param = (new_comment, videoId,id)
    cur.execute(query, param)
    con.commit()
    query = 'update comments set original_word= %s where video_id = %s and id=%s '
    param = (original_word, videoId,id)
    cur.execute(query, param)
    con.commit()
    query = 'update comments set new_word= %s where video_id = %s and id=%s'
    param = (new_word, videoId,id)
    cur.execute(query, param)
    con.commit()

# select word token from videos
def selectWordToken():
    query = "SELECT `new_transcript` from videos"
    cur.execute(query)
    result = cur.fetchall()
    con.commit()
    results = []
    for items in result:
        for item in items:
            results.append(item)
    query ='select `new_comment` from comments'
    cur.execute(query)
    result = cur.fetchall()
    for items in result:
        for item in items:
            results.append(item)
    return results

def SelectCommentswithID(video_id):
    query = 'SELECT `comment` from comments where video_id =%s'
    param = (video_id)
    cur.execute(query, param)
    # 读取数据
    comments_all = cur.fetchall()
    con.commit()
    # 打印数据
    comments = []
    for items in comments_all:
        for item in items:
            # print(item)
            comment = re.sub(r'\n+', ' ', str(item))
            comments.append(comment)
    # print(len(comments),comments)
    query = 'SELECT `id` from comments where video_id =%s'
    param = (video_id)
    cur.execute(query, param)
    # 读取数据
    ids_all = cur.fetchall()
    con.commit()
    # 打印数据
    id_list = []
    for items in ids_all:
        for id in items:
            id_list.append(id)
    return comments,id_list

def insertTopicComment(id, video_id,topic):
    query = 'update commets set topic= %s where id = %s and video_id=%s'
    param = (topic, id,video_id)
    cur.execute(query, param)
    con.commit()

# For sentiment analysis：


def SelectAllComments():
    query = 'SELECT `comment` from comments'
    cur.execute(query)
    # 读取数据
    comments_all = cur.fetchall()
    con.commit()
    # 打印数据
    comments = []
    for items in comments_all:
        for item in items:
            # print(item)
            comment = re.sub(r'\n+', ' ', str(item))
            comments.append(comment)
    # print(len(comments),comments)
    query = 'SELECT `id` from comments'
    cur.execute(query)
    # 读取数据
    ids_all = cur.fetchall()
    con.commit()
    # 打印数据
    id_list = []
    for items in ids_all:
        for id in items:
            id_list.append(id)
    return comments,id_list


def InsertCommentsSAResult( id,neg, neu,pos,compound,sentiment):
    query = 'update comments set neg= %s where  id=%s '
    param = (neg, id)
    cur.execute(query, param)
    con.commit()

    query = 'update comments set neu= %s where id=%s'
    param = (neu, id)
    cur.execute(query, param)
    con.commit()

    query = 'update comments set pos= %s where id=%s'
    param = (pos, id)
    cur.execute(query, param)
    con.commit()

    query = 'update comments set compound= %s where  id=%s'
    param = (compound, id)
    cur.execute(query, param)
    con.commit()

    query = 'update comments set sentiment= %s where id=%s'
    param = (sentiment, id)
    cur.execute(query, param)
    con.commit()

def selectActuralSentiment():
    query = 'SELECT `polarity` from comments where polarity is not null'
    cur.execute(query)
    # 读取数据
    sentiments = cur.fetchall()
    # print(transcripts)
    con.commit()
    # 打印数据
    actural=[]

    # videosContents = ''
    for items in sentiments:
        for item in items:
            actural.append(item)
        # print(item)
    return actural

def selectResultsSentiment():
    query = 'SELECT `sentiment` from comments where polarity is not null'
    cur.execute(query)
    # 读取数据
    sentiments = cur.fetchall()
    # print(transcripts)
    con.commit()
    # 打印数据
    vader_sentiment=[]

    # videosContents = ''
    for items in sentiments:
        for item in items:
            vader_sentiment.append(item)
        # print(item)
    # print(transcript)
    return vader_sentiment


# Close MySQL
def CloseAll():
    cur.close()
    con.close()




# 要删的
def InsertCommentsTestSA(id, polarity, subjectivity):
    query = 'update comments set polarity= %s where id=%s'
    param = (polarity, id)
    cur.execute(query, param)
    con.commit()
    query = 'update comments set subjectivity= %s where id=%s'
    param = (subjectivity, id)
    cur.execute(query, param)
    con.commit()

