from flask import Flask, render_template, request,redirect,send_file
from googleapiclient.discovery import build
from channel_info import get_channel_stats
from videoID import get_video_id
from videoInfo import get_video_details,get_vid_detail
from comments import get_comment_table
from save_images import save_image
from pytube import YouTube
import pymongo
from io import BytesIO
import logging
logging.basicConfig(filename="login.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

try:
    api_key = 'AIzaSyBfQwuMy7eqcGh2tk2jtiw3K0Oxz2g6jtA'
    youtube = build('youtube', 'v3', developerKey=api_key)
    #mydb, cursor = get_database() cant use because heroku will not support
    client = pymongo.MongoClient("mongodb+srv://root:root123@nalla2op.hae1tqo.mongodb.net/?retryWrites=true&w=majority")
    db = client.youtube
    chan_col = db['channel_table']
    vid_col = db['video_table']
    coll = db['youtube data']
except Exception as e:
    logging.error(e)

class channel:
    channel_id = ''

obj_ytube = channel()

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    '''
    :return: it is to render template index.html
    '''
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(e)
        return render_template('error.html')

@app.route('/youtube_path', methods =['POST'])
def find_channel_code():
    '''
    it is used to find the youtube channel id using the Pytube module
    :return: None , redirect to /channel_info
    '''
    try:
        video = YouTube(request.form['url'])
        obj_ytube.channel_id = video.channel_id

        return redirect('/channel_info')
    except Exception as e:
       return render_template('error.html')


@app.route('/channel_info', methods =['GET'])
def channel_info():
    '''
    in this all the data of channel  and 50 videos of that channel are soted in the MYSQL and the comments will be stored in
    the MONGODB
    :return: NONE , redirected to /list_channel
    '''
    try:
        channel_info = get_channel_stats(youtube, obj_ytube.channel_id)

        chan_col.insert_one(channel_info)
        video_ids = get_video_id(youtube, channel_info)
        video_info = get_video_details(youtube, video_ids)
        for i in video_info:
            vid_col.insert_one(i)
        return redirect('/list_channel')
    except Exception as e:
        logging.error(e)
        return render_template('error.html')



@app.route('/list_channel',methods = ['GET'])
def list_channel():
    '''
    This function is used to fetch all the stored channel info from MYSQL DB
    :return: channel.html
    '''
    try:
        a = chan_col.find()
        return render_template('channel.html',var = a)
    except Exception as e:
        logging.error(e)
        return render_template('error.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    '''
    This function is used to fetch all the stored video info from MYSQL DB
    :param path: channel_id
    :return: video_html
    '''
    try:
        a =vid_col.find({'channel_id': path})

        return render_template('videos.html',var = a)
    except Exception as e:
        logging.error(e)
        return render_template('error.html')

@app.route('/videos/', defaults={'path': ''})
@app.route('/videos/<path:path>')
def comment(path):
    '''
    This is used to fetch all the comments from MONGO DB
    :param path: Video_ID
    :return: comment.html
    '''

    try:
        a = coll.find()
        for i in a:
            if i['video_Id'] == path:
                return render_template('comment.html', var = i['comments_id']['comments'])
        else:
            vid_info = get_vid_detail(youtube, path)
            comment_table = get_comment_table(youtube, vid_info)
            img_b64 = save_image(vid_info)

            for i in range(len(img_b64)):
                data_mongo = {
                    'video_Id': img_b64[i]['video_id'],
                    'img_base64_encoded': img_b64[i]['img_b64'],
                    'comments_id': comment_table[i]
                }
                coll.insert_one(data_mongo)
                return redirect(f'/videos/{path}')
        return render_template('base.html')
    except Exception as e:
        logging.error(e)
        return render_template('error.html')

@app.route('/download/', defaults={'path': ''})
@app.route('/download/<path:path>')
def download_video(path):
    '''
    this function is used to download the youtube video
    :param path: video_id
    :return: NONE redirect to the /list_channel
    '''
    try:
        buffer = BytesIO()
        path = 'https://www.youtube.com/watch?v='+path
        video = YouTube(path)
        video = video.streams.get_highest_resolution()
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment = True, download_name= 'video.mp4', mimetype='video/mp4')
    except Exception as e:
        logging.error(e)
        return render_template('error.html')


@app.route('/image/',defaults={'path': ''})
@app.route('/image/<path:path>')
def image(path):
    try:
        a = coll.find()
        for i in a:
            if i['video_Id'] == path:
                return render_template('images.html', image= i['img_base64_encoded'])
        return render_template('base.html')
    except Exception as e:
        logging.error(e)
        return render_template('error.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=50001, debug=True)
	#app.run(debug=True)


