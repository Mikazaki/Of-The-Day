from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import random
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os

app = Flask(__name__)
Bootstrap5(app)

scheduler = BackgroundScheduler(timezone="UTC", daemon=True)

def write_daily_item(file_name, range_end):
    items = list(range(1, range_end))
    random.shuffle(items)
    item = items[0]
    
    with open(file_name, 'w') as f:
        f.write(str(item))

def get_daily_item(file_name, range_end):
    if not os.path.exists(file_name):
        write_daily_item(file_name, range_end)
    with open(file_name, 'r') as f:
        return int(f.read().strip())

scheduler.add_job(lambda: write_daily_item('daily_verse.txt', 6237), 'cron', hour=0)
scheduler.add_job(lambda: write_daily_item('hadith.txt', 7564), 'cron', hour=0)
scheduler.start()



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/verse')
def verse():
    reciters = ['alafasy', 'abdurrahmaansudais', 'muhammadayyoub', 'mahermuaiqly']


    url = f"https://api.alquran.cloud/v1/ayah/{get_daily_item('daily_verse.txt', 6237)}/editions/quran-uthmani,en.hilali"

    response = requests.get(url)

    data = response.json()

    arabic = data['data'][0]['text']
    english = data['data'][1]['text']
    vno = data['data'][0]['numberInSurah']
    chapter = data['data'][0]['surah']['englishName']
    
    reciter_audios = {}
    for reciter in reciters:
        url_2 = f'https://api.alquran.cloud/v1/ayah/{get_daily_item("daily_verse.txt", 6237)}/ar.{reciter}'
        response_2 = requests.get(url_2)
        data_2 = response_2.json()
        reciter_name = data_2['data']['edition']['englishName']
        reciter_audios[reciter_name] = data_2['data']['audio']


    return render_template("quran.html", verse=arabic, translation=english, verse_num=vno, chapter=chapter, audios=reciter_audios)


@app.route('/hadith')
def hadith():
    
    url = f"https://random-hadith-generator.vercel.app/bukhari/{get_daily_item('hadith.txt', 7564)}"

    response = requests.get(url)

    data = response.json()

    text = data['data']['hadith_english']
    refno = data['data']['refno']
    narrator = data['data']['header']
    
    return render_template('hadith.html', text=text, reference=refno, narrator=narrator)


if __name__ == "__main__":
    app.run(debug=True)
