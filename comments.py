import logging

logging.basicConfig(filename="login.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")


def get_comment_table(youtube,video_info):
    '''
    It will return a dictionary for a list of comment for all the videos from the channel
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param video_info: <list> of <dict>, It contains all the info about videos of a specific channel
    :return: <list> comment_table, list of comments of all the video(max 50) in the channel
    '''
    try:
        comment_table = []
        for id in video_info:
            comment = []
            if int(id['comments'])>0:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId= id['video_id'])

                response = request.execute()
                for com in response['items']:
                    comments = dict(
                        comment_text = com['snippet']['topLevelComment']['snippet']['textDisplay'],
                        author = com['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                    comment.append(comments)

            else:
                comment =[]
            comment_per_video= dict(
                video_id = id['video_id'],
                comments = comment)
            comment_table.append(comment_per_video)

            logging.info(f"The comments are fetched")
        return comment_table

    except Exception as e:
        logging.error(f" An Error occured while retriving comments : {e} ")