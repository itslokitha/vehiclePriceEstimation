import schedule
import time
import os

def task_2am():
    os.system("Extraction.py")

def task_5am():
    os.system("dataTransformation.py")

schedule.every().day.at("02:00").do(task_2am)
schedule.every().day.at("05:00").do(task_5am)

while True:
    schedule.run_pending()
    time.sleep(1)