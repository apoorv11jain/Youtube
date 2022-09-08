import logging

logging.basicConfig(filename="login.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")


def get_channel_stats(youtube, channel_id):
    '''
    This fuction is used to provide the channel information required to fetch videos and comments using youtube api
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param channel_id: type: <String>, It is the id that act as a primary key for all the youtube channel
    :return: type: <Dictionary>, The dictionary contains all the required data fetched using youtube api
    '''
    try:
        request = youtube.channels().list(
            part = 'snippet,contentDetails,statistics',
            id = channel_id
        )
        response = request.execute()
        channel_info = dict(
        channelid = channel_id,
        channel_name = response['items'][0]['snippet']['title'],
        play_list = response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
        view_count = int(response['items'][0]['statistics']['viewCount']),
        subscriber_count =int(response['items'][0]['statistics']['subscriberCount']),
        videocount = int(response['items'][0]['statistics']['videoCount'])
        )

        logging.info(f"the channel info are {channel_info}")
        return channel_info
    except Exception as e:
        logging.error(f"An error occured when retirving info {e}")


if __name__=='__main__':
    from googleapiclient.discovery import build
    api_key = 'AIzaSyBfQwuMy7eqcGh2tk2jtiw3K0Oxz2g6jtA'
    youtube = build('youtube', 'v3', developerKey=api_key)
    print(youtube)
    print(get_channel_stats(youtube,'UCzImuz4bhgz07u_4TRYedGg'))