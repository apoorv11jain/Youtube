import base64
import requests
import logging
logging.basicConfig(filename="login.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")


def save_image(video_info):
    '''
    It is used to fetch the image and convert it into the base 64.
    :param video_info: <list> of <dict>, It contains all the info about videos of a specific channel
    :return: <list> of <dict> ,  with image in base64
    '''
    try:
        img_b64s =[]
        for i in video_info:
            r = requests.get(i['img_url']).content
            image = dict(
                    img_b64 = base64.b64encode(r),
                    video_id = i['video_id'])
            img_b64s.append(image)
        logging.info("The images are been changed to base64")
        return img_b64s
    except Exception as e:
        logging.error(f"An error occured {e}")


