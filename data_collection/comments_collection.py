import random

from util import mysql
import requests
import time

import json


def CommentExtract(videoId, count, key):
    key = key
    YOUTUBE_IN_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={pageToken}&videoId={videoId}&key={key}'
    YOUTUBE_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&videoId={videoId}&key={key}'

    page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key), timeout=10)

    while page_info.status_code != 200:
        if page_info.status_code != 429:
            print(videoId, "Comments disabled")
            result = "Comments disabled"
            return result
        # sleep 10s and try again
        time.sleep(10)
        page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key), timeout=10)
    # get json
    page_info = page_info.json()
    comments = []
    temp = 0
    # go to next page.
    while 'nextPageToken' in page_info:
        temp_page_info = page_info
        page_info = requests.get(YOUTUBE_IN_LINK.format(videoId=videoId, key=key, pageToken=page_info['nextPageToken']),
                                 timeout=10)
        try_time = 0
        while page_info.status_code != 200:
            time.sleep(10)
            page_info = requests.get(
                YOUTUBE_IN_LINK.format(videoId=videoId, key=key, pageToken=temp_page_info['nextPageToken']), timeout=20)
            try_time += 1
            if try_time > 10:
                print(videoId, ': have tried', try_time)
                page_info = temp_page_info
        page_info = page_info.json()
        for i in range(len(page_info['items'])):
            # classify comments, only remain comments with likes >=50
            if page_info['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'] >= 50:
                snippet = page_info['items'][i]['snippet']['topLevelComment']['snippet']
                # print(snippet)
                comment = snippet['textOriginal']
                if len(comment.split()) >= 50:
                    comments.append(comment)
                    temp = temp + 1
                # print(comments)
                # print(len(comments))
            if temp == count:
                return comments
    return comments


def CommentsCollection():
    # videos cannot get
    falls = []
    key= 'AIzaSyC36OpHwDuHGrx3UMW-Rr4MXn0e025hEhQ'


    # count:the max number of comments for each video
    count = 500
    for i in range(0, 5):
        videoIds = mysql.SelectVideoIDforComments()
        print('the number of videos we still need to collect:', len(videoIds))

        for videoId in videoIds:
            try:
                comments = CommentExtract(videoId, count, key)
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
                if comments == 'Comments disabled':
                    falls.append(videoId)
            except Exception as e:
                falls.append(videoId)
                print(videoId, ' : ', e)
                pass
            continue

    with open(f'falls_comments.json', 'w', encoding='utf-8') as json_file:
        json.dump(falls, json_file)
