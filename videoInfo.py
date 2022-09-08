import logging
logging.basicConfig(filename="login.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

def get_video_details(youtube,video_id):
    '''
    This function is used to get video info Using the Youtube Api
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param video_id: <dict> of <list> it contains all the video Id from a channel
    :return: <list> of <dict> , it is contains required info of the video
    '''
    try:
        video_info = []
        request = youtube.videos().list(
            part = 'snippet,statistics',
            id = ','.join(video_id['video_ids'])
        )
        response =request.execute()
        for video in response['items']:
            video_stats = dict(
                               channel_id = video_id['channel_id'],
                               Title = video['snippet']['title'],
                               Views = int(video['statistics']['viewCount']),
                               Likes = int(video['statistics']['likeCount']),
                               comments = int(video['statistics']['commentCount']),
                               img_url =  video['snippet']['thumbnails']['high']['url'],
                               video_link = 'https://www.youtube.com/watch?v='+video['id'],
                               video_id = video['id']
                               )
            video_info.append(video_stats)
        logging.info(f"The Video Info are fetched")
        return video_info
    except Exception as e:
       logging.error(f"An Error occured while retriving video info : {e}")


def get_vid_detail(youtube,video_id):
    '''
    This function is used to get video info Using the Youtube Api
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param video_id: <string> it contains one video Id
    :return: <list> of <dict> , it is contains required info of the video
    '''
    try:
        video_info = []
        request = youtube.videos().list(
            part = 'snippet,statistics',
            id = video_id
        )
        response =request.execute()
        for video in response['items']:
            video_stats = dict(
                               Title = video['snippet']['title'],
                               Views = int(video['statistics']['viewCount']),
                               Likes = int(video['statistics']['likeCount']),
                               comments = int(video['statistics']['commentCount']),
                               img_url =  video['snippet']['thumbnails']['high']['url'],
                               video_link = 'https://www.youtube.com/watch?v='+video['id'],
                               video_id = video['id']
                               )
            video_info.append(video_stats)
        logging.info(f"The Video Info are fetched")
        return video_info
    except Exception as e:
       logging.error(f"An Error occured while retriving video info : {e}")

