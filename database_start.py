import mysql.connector as connection
import logging
logging.basicConfig(filename="login.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")


def get_database():
    '''
    This Function is used to get the database connector. It will declare the table and database if not present already
    :return: <mysql.connector.connection.MySQLConnection object at 0x0000028357BC4B70> , MySQLCursor

    '''
    try:
        mydb = connection.connect(host='localhost',  user='root', passwd='root123', use_pure=True)
        cursor = mydb.cursor()
        cursor.execute('Create database youtube;')
        mydb = connection.connect(host='localhost', database='youtube', user='root', passwd='root123', use_pure=True)
        query1 = 'Create Table channel_infos(Channel_Id varchar(50) NOT NULL, Channel_name varchar(100), Playlist varchar(50), View_count bigint, Subscriber_count bigint, video_count bigint);'
        query2 = 'Create Table Video_info( Video_title varchar(100), Video_view bigint, video_likes bigint, video_comment_count bigint, thumbnail_url varchar(300), video_url varchar(300), video_id varchar(50) NOT NULL,channel_id varchar(50));'
        cursor = mydb.cursor()
        cursor.execute(query1)
        cursor.execute(query2)
        logging.info("Database created")
        logging.info("tables created")

    except Exception as e:
        try:
            mydb = connection.connect(host='localhost', database='youtube', user='root', passwd='root123',use_pure=True)
            query1 = 'Create Table channel_infos(Channel_Id varchar(50), Channel_name varchar(100), Playlist varchar(50), View_count int, Subscriber_count int, video_count int);'
            query2 = 'Create Table Video_info( Video_title varchar(100), Video_view int, video_likes int, video_comment_count int, thumbnail_url varchar(300), video_url varchar(300), video_id varchar(50),channel_id varchar(50));'
            cursor = mydb.cursor()
            cursor.execute(query1)
            cursor.execute(query2)
            logging.info("Tables created")
        except Exception as e:
            mydb = connection.connect(host='localhost', database='youtube', user='root', passwd='root123',use_pure=True)
            cursor = mydb.cursor()
            logging.info("connection established")
    return mydb, cursor

