import random
from data_collection import comments_collection as CD, transcription__collection
from tools import mySQL


# import sys
# import Comments
# import json

def dataCollecting():
    # Collect transcripts：
    # for i in range(0,2):
    #     transcription__collection.TranscriptionCollection()

    # Collect comments：
    # for 3 p.m. /day
    videoIds = mySQL.SelectVideoIDforComments()
    print( ' number of videos need to be collected: ', len(videoIds))
    CD.CommentsCollection(videoIds)

    mySQL.CloseAll()
