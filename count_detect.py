import psycopg2
import cv2
import os.path

def db_connection():
    conn = psycopg2.connect( # соед с БД
        host="postgres",
        database="db_track",
        user="admindb",
        password="pass",
        port="5432"
    )
    return conn

def count(filename):
    conn = db_connection() #соед
    cur = conn.cursor() # курсор нужен для обращения к БД
    cur.execute('CREATE TABLE IF NOT EXISTS data (id SERIAL NOT NULL,' # создаем таблицу 
                'filename VARCHAR NOT NULL,'                #создание столбцов VARCHAR-тип файла          
                'duration_video VARCHAR NOT NULL,'          #создание столбцов duration_video-длительность видео 
                'statistic VARCHAR NOT NULL);'              #создание столбцов statistick - статистика общее количество задетектированных
                                                            #объектов на 1 кадре
                )
    conn.commit() # внесение изменений
    TXTFILE = f'{os.path.join(os.path.dirname(__file__))}/results/{filename[:-4]}.txt' # путь к текст файлу с результатами
    MP4FILE = f'{os.path.join(os.path.dirname(__file__))}/results/{filename}'          # путь к файлу с видео результатом
    video = cv2.VideoCapture(MP4FILE) # ля читки видео файла для далнейшей обработки
    fps = video.get(cv2.CAP_PROP_FPS)  # частота файлов
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT) # Количество кадров
    seconds = frame_count / fps # секунды
    minutes = int(seconds / 60) # минуты
    rem_sec = int(seconds % 60) #
    duration = f"{minutes}:{rem_sec}" # длительность видео
    with open(TXTFILE) as file:  # открывает файл TXTFILE
        sum_detect = sum([1 for _ in file])
    cur.execute('INSERT INTO data (filename, duration_video, statistic)' # вносим данныи статистику
                'VALUES (%s, %s, %s);',
                (f'{filename}',
                 f'{duration}',
                 f'{sum_detect}')
                )
    conn.commit() # внесение изменений
