import random
from data_collection import comments_collection as CD
from data_collection import transcription_collection
from util import mysql



def dataCollecting():
    # Collect transcripts：
    transcription_collection.TranscriptionCollection()

    # Collect comments：
    # for 3 p.m. /day
    CD.CommentsCollection()


