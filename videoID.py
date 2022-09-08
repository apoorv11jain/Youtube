import logging
logging.basicConfig(filename="login.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")


def get_video_id(youtube, channel_info):
    '''
    this function is used to get all the video id from the channel
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param channel_info: <dict> containing the data of a channel
    :return: <dict> of <list> it contains all the video Id from a channel
    '''
    try:
        video_ids = []
        request = youtube.playlistItems().list(
            part = 'contentDetails',
            playlistId = channel_info['play_list'],
            maxResults =50
        )
        response = request.execute()

        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])
        logging.info(f"The video Id are fetched")
        return dict(channel_id = channel_info['channelid'],
                    video_ids = video_ids)
    except Exception as e:
        logging.error(f"An error occured while retriving video Id : {e}")