import re
import util.mysql as mysql



# 清除description中的不必要的数据（URL/email/Twitter/Instagram/Facebook/Snapchat）
# 清除URL（字母://）或者www
def cleanURL(strToClean):
    weblink = re.compile(r'[a-zA-z]+://[^\s]*', re.S)
    strToClean = re.sub(weblink, ' ', strToClean)
    weblink1 = re.compile(r'www.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
    strToClean = re.sub(weblink1, ' ', strToClean)
    return strToClean
    # print(strToClean)


# clean email
def cleanEmail(strToClean):
    email = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-z0-9-.]+)', re.S)
    strToClean = re.sub(email, ' ', strToClean)
    # print(strToClean)
    return strToClean


# @开头的channel name
def cleanChannelName(strToClean):
    channel = re.compile(r'@[a-zA-Z0-9-]+', re.S)
    strToClean = re.sub(channel, ' ', strToClean)
    # print(strToClean)
    return strToClean


# 替换连续的符号\空格、换行
def cleanSymbols(strToClean):
    # 替换连续的空格
    strToClean = re.sub(' +', ' ', strToClean)
    strToClean = re.sub(r'\n+', ' ', strToClean)

    # print(len(strToClean),strToClean)
    return strToClean


# clean transcripts and comments of each video. save them into original place
def dataCleaning():
    print('Start to clean Transcripts: ')
    videoIds = mysql.SelectVideoID()
    print('the number we need to clean: ', len(videoIds))
    for videoID in videoIds:
        transcript = mysql.selectTranscripts(videoID)
        transcript = cleanSymbols(transcript)
        mysql.updateCleanedTranscripts(videoID, transcript)
        if videoIds.index(videoID)%100==1:
            print('    number of videos complete: ',videoIds.index(videoID)+1)
    print(' All Transcripts Cleaned!')

    print('Start to clean Comments: ')
    comments, id_list=mysql.SelectAllComments()
    print('the number we need to clean: ', len(comments))

    for index in range(len(comments)):
        comment=comments[index]
        id = id_list[index]

        comment = cleanURL(comment)
        comment = cleanChannelName(comment)
        comment = cleanSymbols(comment)
        mysql.updateCleanedCommentsToComments(id, comment)
        if index %1000==1:
            print('    number of comments complete: ',index+1)
    print(' All Comments Cleaned!')

    # delete the comments not reach our requests
    comments, id_list = mysql.SelectAllComments()
    print(len(comments))
    temp=0
    for index in range(len(comments)):
        comment = comments[index]
        id = id_list[index]
        if len(comment.split()) <50:
            temp+=1
            print('we have delete: ',temp
                  )
            mysql.delCommentsLessThan30(id)
    print('final comments:',len(comments)- temp)

