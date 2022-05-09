from util import mysql as mysql
import json


# 选择合适的视频：
def dataClassificationWithTags():
    videoIds = mysql.SelectVideoID()

    tagswithFrequency = {'tags': 0}

    for i in range(0, len(videoIds)):
        videoId = videoIds[i]
        # print(videoId)
        tag = mysql.selectTags(videoId)
        tag = tag.lower()
        tags=[]
        if tag == '[none]':
            tags = []
        else:
            tags = tag.split('|')

        # print(tags)
        for tag in tags:
            tagswithFrequency['tags'] = tagswithFrequency['tags'] + 1
            # print('tagswithFrequency[tags]: ', tagswithFrequency['tags'])
            if tag in tagswithFrequency.keys():
                # print('tagswithFrequency[tag]:' ,tagswithFrequency[tag])
                tagswithFrequency[tag] = tagswithFrequency[tag] + 1
                # print('new tagswithFrequency[tag]', tagswithFrequency[tag])
            if tag not in tagswithFrequency.keys():
                tagswithFrequency.update({tag: 1})
                # print(tagswithFrequency)
        # print(videoId,tagswithFrequency)
        new_tags = ' , '.join(tags)
        mysql.insertNewTags(videoId, new_tags)
        print(i)
    print(tagswithFrequency)
    tagswithFrequency = sorted(tagswithFrequency.items(), key=lambda item: item[1], reverse=True)
    tagswithFrequency = tagswithFrequency[:30]
    with open(f'tags.json', 'w', encoding='utf-8') as json_file:
        json.dump(tagswithFrequency, json_file)

    tagsF = []
    for items in tagswithFrequency:
        for i in range(items[1]):
            tagsF.append(items[0])
    print(tagsF)

