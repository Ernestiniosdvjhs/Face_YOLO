import os.path
from flask import *
from werkzeug.utils import secure_filename
import time
import count_detect


UPLOAD_FOLDER = f'{os.path.join(os.path.dirname(__file__))}/uploads/'#путь к папке куда сохраняется видео, загруженное пользователем
RESULTS = f'{os.path.join(os.path.dirname(__file__))}/results'#путь куда переносятся последний результат трекинга
OUTPUT = f'{os.path.join(os.path.dirname(__file__))}/static/output'#путь к видео, которое будет выводится на сайт
FOLDER_WITH_FILE = f'{os.path.join(os.path.dirname(__file__))}/runs/track'#путь, где изначально сохраняется результат
ALLOWED_EXTENSIONS = {'mp4'}#Расширения файлов, которые можно загрузить

app = Flask(__name__)
app.config['SECRET_KEY']= 'DKcd8!@ks_daHAFg'#секретный ключ


def track(file, filename):#трекинг файла
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    os.system(f'python3 track.py --source uploads/{filename} --yolo_model weights.pt --save-vid --save-txt')#команда трекинга
    os.remove(f'uploads/{filename}')#удаляет файл загруженный пользователем из папки uploads
    if len(os.listdir(RESULTS))>0:#удаляет прошлые результаты трекинга, если они есть в папке с результатами
        os.system(f'rm -rf {RESULTS}/*')
    if len(os.listdir(OUTPUT))>0:#удаляет прошлые результаты трекинга, если они есть в папке с результатами
        os.system(f'rm -rf {OUTPUT}/*')
    FILE = f'{os.path.join(os.path.dirname(__file__))}/runs/track/weights_osnet_x0_25/{filename}'#Путь к папке weights_osnet_x0_25, где хранится результат .mp4
    TXTFILE = f'{os.path.join(os.path.dirname(__file__))}/runs/track/weights_osnet_x0_25/tracks/{filename[:-4]}.txt'#Путьк папке tracks, где хранится результат .txt
    time.sleep(20)
    os.system(f'cp {FILE} {RESULTS}')#копирует mp4 файл из FILE в папку с результатами
    os.system(f'cp {TXTFILE} {RESULTS}')#копирует txt файл из FILE в папку с результатами
    os.system('rm -rf runs/track/*')#удаляет все файлы в папке runs/track
    os.system(f'ffmpeg -i results/{filename} -vcodec libx264 -acodec aac static/output/output.mp4')
    count_detect.count(filename)#вызывает функцию count, где данные добавляются в бд
    return redirect('/result/')

@app.route('/', methods=['GET'])
def index():
    return redirect("/main")



@app.route('/main', methods=['POST', 'GET'])#главная страница
def page_main():
    if request.method == 'POST':
        if request.form.get('main'):
            return redirect('/main')#перекидывает на главную страницу
        elif request.form.get('info'):
            return redirect('/info/')#перекидывает на страницу с информацией
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)#Защита от изменения файловой системы сервера от пользователя
            if filename.split('.')[1] not in ALLOWED_EXTENSIONS:#если файла не подходит, то выводится сообщение об ошибке
                flash('Неправильный формат файла. Пожалуйста, выберите файл формата .mp4', category='error')
            else:
                return track(file, filename)#вызывает функцию скачивания файла
        else:
            flash('Нет выбранного файла', category='nofile')#если файла нет, то выводится сообщение о том, что файл не выбран.
    return render_template('main.html')#отображает main.html


@app.route('/result/', methods=['POST', 'GET'])#страница, где отображается результат
def result():
    if request.method == 'POST':
        if request.form.get('main'):
            return redirect('/main')
        elif request.form['install']:
            app.config['OUTPUT'] = OUTPUT
            return send_from_directory(app.config['OUTPUT'], 'output.mp4', as_attachment=True)
    return render_template('result.html')


@app.route('/info/', methods=['GET', 'POST'])#информация о проекте
def page_about_us():
    if request.method == 'POST':
        if request.form.get('main'):#перекидывает на главную страницу
            return redirect('/main')
        elif request.form.get('info'):
            return redirect('/info/')#перекидывает на страницу с информацией
    return render_template('info.html')#отображает info.html


if __name__ == '__main__':#запускает app.py
    app.run(host='0.0.0.0', port=8888)
