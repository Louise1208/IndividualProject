import random

from youtube_transcript_api import YouTubeTranscriptApi
from util import mysql
import json


def GetTranscription(videoIds):
    fal = []
    temp = 0

    for index, videoId in enumerate(videoIds):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(videoId)
            transcripts = ''
            for i in transcript:
                # print(i)
                text = i['text']
                # print(text)
                transcripts = transcripts + text + ' '
            if len(transcripts.split()) > 30:
                mysql.InsertTranscriptInf(videoId, transcripts)
                # print(transcripts)
                # transcription[index]=transcription
            temp = temp +1
            print(temp, '!!!!!!!!!!!!!!!!!!!!OK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        except:
            #videos cannot collect
            fal.append(videoId)
            print(len(fal))
    # print(fal)
    return fal

# transcript collext
def TranscriptionCollection():
    videoIds = mysql.SelectVideoIDforThanscripts()
    random.shuffle(videoIds)
    print(len(videoIds))
    falls = GetTranscription(videoIds)
    print(len(falls))
    videoIds=falls
    fallsrecord = GetTranscription(videoIds)
    with open(f'falls_transcripts.json', 'w', encoding='utf-8') as json_file:
        json.dump(fallsrecord, json_file)
    print(fallsrecord)
    print('transcript collect!')

