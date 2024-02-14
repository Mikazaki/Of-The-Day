import requests
import random

hadiths = list(range(1, 7564))

random.shuffle(hadiths)


for hadith in hadiths:
    hadith

url = f"https://random-hadith-generator.vercel.app/bukhari/{hadith}"

response = requests.get(url)

data = response.json()

text = data['data']['hadith_english']
refno = data['data']['refno']
narrator = data['data']['header']

print(text)
print(refno)
print(narrator)
