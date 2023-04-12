import requests  # 进行请求
import time  # 注意网站的反爬机制
import pymysql
import random
from bs4 import BeautifulSoup


agent_list = [
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10"
]

def random_id(id_len):
    all_id = '123456789'
    last_pos = len(all_id) - 1
    author_id = ''
    for _ in range(id_len):  # 随机生成n位id
        index = random.randint(0, last_pos)
        author_id = author_id + all_id[index]
    return author_id

def random_name(id_len):
    all_name = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    last_pos = len(all_name) - 1
    author_name = ''
    for _ in range(id_len):  # 随机生成n位id
        index = random.randint(0, last_pos)
        author_name = author_name + all_name[index]
    return author_name

def get_html(url):
    # 构建请求头，伪装成浏览器
    db_headers = {'User-Agent': random.choice(agent_list), 'referer': 'https://book.douban.com/'}
    basic_url = url
    db_novel = requests.get(url=basic_url, headers=db_headers)
    db_novel_html = db_novel.text
    return db_novel_html

def parse_html_comments(db_html,bookid):
    bs = BeautifulSoup(db_html, 'html.parser')
    grid_view = bs.find_all('li', class_="comment-item")

    for item in grid_view:
        cid_random = random_id(7)
        comments = item.find('span', class_="short").text
        comments = str(comments).replace("”","")
        comments = str(comments).replace("“", "")
        comments = str(comments).replace("'", "")

        tzuozhe = item.find('span', class_="comment-info")
        ping = tzuozhe.find('span')
        if len(str(ping)) != 60:
            star = 5
        else:
            if ping.get('title') == "还行":
                star = 3
            elif ping.get('title') == "力荐":
                star = 5
            elif ping.get('title') == "推荐":
                star = 4
            elif ping.get('title') == "较差":
                star = 2
            else:
                star = 1
        uid = random_id(2)
        uname = random_name(7)
        cursor.execute("insert ignore into user(uid,uname) values (%s,%s)",(uid, uname))
        cursor.execute("insert ignore into comment(cid,uid,bid,cstar,cdesc) values (%s,%s,%s,%s,%s)",(cid_random,uid,str(bookid),star,comments))
        conn.commit()


conn = pymysql.connect(host='127.0.0.1', user='root', password='root', port=3306, database='bookrec', charset='utf8')
cursor = conn.cursor()
sql = "SELECT bid FROM book"
cursor.execute(sql)

results = cursor.fetchall()
i = 0
for row in results:

    basic_url = 'https://book.douban.com/subject/{}/comments/'.format(row[0])
    time.sleep(random.uniform(1, 2.5))
    db_html = get_html(basic_url)
    parse_html_comments(db_html, row[0])
    print('换一本书',i)
    i +=1



cursor.close()
conn.close()