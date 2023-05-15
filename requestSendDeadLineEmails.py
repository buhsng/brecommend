import requests
from threading import Thread
import time
url = 'http://127.0.0.1:8000/index/sentdeadlines/'

def requestSendEmails():
    res=requests.get(url)
    print("status：",res.status_code)
    
if __name__=="__main__":
    def func():
        while True:
            requestSendEmails()
            time.sleep(60)
    t = Thread(target=func)
    t.start()
    t.join()
