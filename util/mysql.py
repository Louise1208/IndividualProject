import re

import pymysql

# connect database
con = pymysql.connect(host='121.199.58.129',
                      port=3306,
                      user='root',  # mysql的登录账号admin
                      password='991208',  # mysql的登录密码pwd
                      db='youtube')  # mysql中要访问的数据表

cur = con.cursor()


# Data Collection：
def SelectVideoID():

    query = "SELECT `video_id` from videos"
    cur.execute(query)

    videoId = cur.fetchall()

    videoIds = []
    for items in videoId:
        for item in items:
            if item not in videoIds:
                videoIds.append(item)
    # print(videoIds)
    return videoIds


# select transcripts without video_id
def SelectVideoIDforThanscripts():
    # print('try to select video id for transcripts')

    query = "select video_id from videos where video_id not in (select video_id from transcripts) "
    # query = 'select video_id from comments where video_id not in (select video_id from transcripts) order by likes desc'
    cur.execute(query)
    con.commit()

    videoId = cur.fetchall()

    videoIds = []
    for items in videoId:
        for item in items:
            videoIds.append(item)
    # print(len(videoIds))
    return videoIds


# collect transcript
def InsertTranscriptInf(videoId, transcription):
    # 执行sql语句
    query = 'insert into transcripts(`video_id`,`transcript`) values(%s,%s) '
    param = (videoId, transcription)
    cur.execute(query, param)
    con.commit()
    # print(videoId + 'GB Video transcription collect!')


def SelectVideoIDforComments():
    # print('try to select video id for transcripts')

    query1 = 'create table tem_comments (select DISTINCT video_id from comments)'
    cur.execute(query1)
    con.commit()
    videoIds = []

    query2 = "select video_id from all_videos where video_id not in (select video_id from tem_comments) and video_id not in (select video_id from videos_without_comments) "
    cur.execute(query2)
    con.commit()
    # print(len(videoIds))
    videoId = cur.fetchall()

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



def insertVideoswithoutComments(videoId):
    # print('start')
    query = 'insert into videos_without_comments (`video_id`) value(%s)'
    param = (videoId)
    cur.execute(query, param)
    con.commit()
    # print('insert!!')


# insert comments
def InsertComments(videoid, comment):

    query = 'insert into comments(`video_id`,`comment`) values(%s, %s)'
    param = (videoid, comment)
    cur.execute(query, param)
    con.commit()


# For Data Selection
# Get tags
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


# insert tags to videos
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
    transcripts = cur.fetchall()
    # print(transcripts)
    con.commit()

    videosContents = []
    # videosContents = ''
    for items in transcripts:
        for item in items:
            videosContents.append(item)
        # print(item)
    transcript = ','.join(videosContents)
    # print(videoId,transcript)
    return transcript


# # insert cleaned comments：
def updateCleanedCommentsToComments(id, comment):

    query = 'update comments set `comment` = %s where id=%s'
    param = (comment, id)
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
    videos = cur.fetchall()
    con.commit()

    videosContents = []
    for items in videos:
        for item in items:
            videosContents.append(item)
    # print(videosContents)
    videosContent = '.'.join(videosContents)
    # print(videosContent)
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
def insertNewComments(id, new_comment, original_word, new_word):
    query = 'update comments set new_comment= %s where  id=%s'
    param = (new_comment, id)
    cur.execute(query, param)
    con.commit()
    query = 'update comments set original_word= %s where  id=%s '
    param = (original_word,id)
    cur.execute(query, param)
    con.commit()
    query = 'update comments set new_word= %s where  id=%s'
    param = (new_word, id)
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
    query = 'select `new_comment` from comments'
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
    comments_all = cur.fetchall()
    con.commit()

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
    ids_all = cur.fetchall()
    con.commit()

    id_list = []
    for items in ids_all:
        for id in items:
            id_list.append(id)
    return comments, id_list


def insertTopicComment(id, topic,possibility):
    query = 'update comments set topic= %s where id = %s'
    param = (topic, id)
    cur.execute(query, param)

    query = 'update comments set possibility= %s where id = %s'
    param = (possibility, id)
    cur.execute(query, param)
    con.commit()


def insertTopicTranscript(videoId, topic,possibility):
    query = 'update videos set topic= %s where video_id = %s'
    param = (topic, videoId)
    cur.execute(query, param)

    query = 'update videos set possibility= %s where video_id = %s'
    param = (possibility, videoId)
    cur.execute(query, param)
    con.commit()


# For sentiment analysis：


def SelectAllComments():
    query = 'SELECT `comment` from comments'
    cur.execute(query)
    comments_all = cur.fetchall()
    con.commit()

    comments = []
    for items in comments_all:
        for item in items:
            # print(item)
            comment = re.sub(r'\n+', ' ', str(item))
            comments.append(comment)
    # print(len(comments),comments)
    query = 'SELECT `id` from comments'
    cur.execute(query)
    ids_all = cur.fetchall()
    con.commit()
    id_list = []
    for items in ids_all:
        for id in items:
            id_list.append(id)
    return comments, id_list


def InsertCommentsSAResult(id, compound, sentiment):
    query = 'update comments set compound= %s where  id=%s'
    param = (compound, id)
    cur.execute(query, param)
    con.commit()

    query = 'update comments set sentiment= %s where id=%s'
    param = (sentiment, id)
    cur.execute(query, param)
    con.commit()


def InsertVideosSAResult(videoId, compound, sentiment):
    query = 'update videos set compound= %s where  video_id=%s'
    param = (compound, videoId)
    cur.execute(query, param)
    con.commit()

    query = 'update videos set sentiment= %s where video_id=%s'
    param = (sentiment, videoId)
    cur.execute(query, param)
    con.commit()

def selectActuralSentiment():
    query = 'SELECT `polarity` from comments where polarity is not null'
    cur.execute(query)
    sentiments = cur.fetchall()
    con.commit()

    actural = []
    # videosContents = ''
    for items in sentiments:
        for item in items:
            actural.append(item)
        # print(item)
    query = 'SELECT `polarity` from videos where polarity is not null'
    cur.execute(query)
    sentiments = cur.fetchall()
    for items in sentiments:
        for item in items:
            actural.append(item)

    con.commit()
    return actural


def selectResultsSentiment():
    query = 'SELECT `sentiment` from comments where polarity is not null'
    cur.execute(query)
    sentiments = cur.fetchall()
    # print(transcripts)
    con.commit()

    vader_sentiment = []

    for items in sentiments:
        for item in items:
            vader_sentiment.append(item)

    query = 'SELECT `sentiment` from videos where polarity is not null'
    cur.execute(query)
    sentiments = cur.fetchall()
    con.commit()
    for items in sentiments:
        for item in items:
            vader_sentiment.append(item)

    return vader_sentiment



def delCommentsLessThan30(id):
    query = 'delete from comments where id=%s'
    param=(id)
    cur.execute(query,param)
    con.commit()


def delTranscriptsLessThan30(videoid):
    query = 'delete from videos where video_id=%s'
    param=(videoid)
    cur.execute(query,param)
    con.commit()




# Close MySQL
def CloseAll():
    cur.close()
    con.close()

def InsertCommentsTestSA(id, polarity):
    query = 'update comments set polarity= %s where id=%s '
    param = (polarity, id)
    cur.execute(query, param)
    con.commit()

def InsertVideosTestSA(id, polarity):
    query = 'update videos set polarity= %s where video_id=%s '
    param = (polarity, id)
    cur.execute(query, param)
    con.commit()
