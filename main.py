from PIL import Image
import requests
from datetime import *
import schedule
import os

#CONSTANTS
letters = 'абвг'
diff = 938 - 272
stroki = [272, 1004, 1736, 2468, 3200, 4006, 4812]
stolb = [0, 816, 1575, 2334, 3093]
a = []
for i in range(5, 12):
    for let in letters:
        a.append(str(i) + let)


def download_image():
    x = datetime.now().day
    try:
        file = open('rasp' + str(x) + '.png')
        file.close()
        return
    except FileNotFoundError:
        url = 'https://амтэк35.рф/wp-content/uploads/shedule/2021-2022/'
        dae = datetime(2021, 9, 1)
        date = datetime.now()
        if(date.weekday() == 6):
            dat = timedelta(days = 1)
            date += dat
        date = max(date, dae)
        url += date.strftime("%d.%m.20%y.png")
        
        res = requests.get(url)
        with open("rasp" + str(x) + ".png", "wb") as f:
            f.write(res.content)
            
        im = Image.open('rasp' + str(x) + '.png')
        for i in range(len(stroki)):
            for let in range(1, 5):
                ij = im.crop((stolb[let - 1], stroki[i], stolb[let], stroki[i] + diff))
                ij.save(str(i + 5) + letters[let - 1] + str(x) + '.png')

#remove images with dairy on previous day
def remove_prev_images():
    prev_date = datetime.now() + timedelta(days=-1)
    
    path = f"*{str(prev_date.day)}.png"
    os.system(f"find . -name {path} -delete")
    
            
        
    
schedule.every().day.at("16:30").do(remove_prev_images)
download_image()
