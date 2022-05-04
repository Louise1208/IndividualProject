from util import mysql
import requests
import time
import sys
import json

YOUTUBE_IN_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={pageToken}&videoId={videoId}&key={key}'
YOUTUBE_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&videoId={videoId}&key={key}'
key = 'AIzaSyC36OpHwDuHGrx3UMW-Rr4MXn0e025hEhQ'


# key='AIzaSyALKx5ModcdJn-WWzJOngzYdKJPrvdx9hg'# key from google api
# key =''# the key from google api.

def CommentExtract(videoId, count):
    page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))

    while page_info.status_code != 200:
        if page_info.status_code != 429:
            print(videoId, "Comments disabled")
            result = "Comments disabled"
            return result
        # sleep 20, and try again
        time.sleep(20)
        page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))
    # get json
    page_info = page_info.json()
    comments = []
    temp = 0
    # go to next page.
    while 'nextPageToken' in page_info:
        page_info = requests.get(YOUTUBE_IN_LINK.format(videoId=videoId, key=key, pageToken=page_info['nextPageToken']))
        while page_info.status_code != 200:
            time.sleep(20)
        page_info = page_info.json()
        for i in range(len(page_info['items'])):
            # classify comments, only remain comments with likes >=200
            if page_info['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'] >= 200:
                snippet = page_info['items'][i]['snippet']['topLevelComment']['snippet']
                # print(snippet)
                comments.append(snippet['textOriginal'])
                # print(snippet['textOriginal'])
                temp += 1
                # print(comments)
                # print(len(comments))
            if temp == count:
                return comments
    return comments


def CommentsCollection(videoIds):
    # 将你想要爬取视频评论的id放入其中
    falls = []

    # count为每个地址想要爬取评论的数目
    count = 500
    for videoId in videoIds:
        try:
            comments = CommentExtract(videoId, count)

            if comments != "Comments disabled":
                print(videoId, len(comments))
                # print('collect! start try insert!')
                if len(comments) == 0:
                    # print('try to del')
                    mysql.insertVideoswithoutComments(videoId)
                else:
                    for comment in comments:
                        # print(comment)
                        mysql.InsertComments(videoId, comment)
                    # print(videoIds.index(videoId) ,' ', videoId, ' Collect!')
        except Exception as e:
            falls.append(videoId)
            print(videoId, ' : ', e)
            pass
        continue
    with open(f'falls_comments.json', 'w', encoding='utf-8') as json_file:
        json.dump(falls, json_file)
