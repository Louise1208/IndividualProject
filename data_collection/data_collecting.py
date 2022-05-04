import random
from data_collection import comments_collection as CD, transcription_collection
from util import mysql


# import sys
# import Comments
# import json

def dataCollecting():
    # Collect transcripts：
    # for i in range(0,2):
    #     transcription__collection.TranscriptionCollection()

    # Collect comments：
    # for 3 p.m. /day
    videoIds = mysql.SelectVideoIDforComments()
    print(' number of videos need to be collected: ', len(videoIds))
    CD.CommentsCollection(videoIds)

    mysql.CloseAll()
