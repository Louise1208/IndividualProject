import random
from data_collection import comments_collection as CD
from data_collection import transcription_collection
from util import mysql



def dataCollecting():
    # Collect transcripts：
    for i in range(0, 2):
        transcription_collection.TranscriptionCollection()

    # Collect comments：
    # for 3 p.m. /day
    videoIds = mysql.SelectVideoIDforComments()
    print(' number of videos need to be collected: ', len(videoIds))
    CD.CommentsCollection(videoIds)

    mysql.CloseAll()
