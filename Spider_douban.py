import requests  # 进行请求
from lxml import etree  # 解析数据
import re  # 数据处理
import time  # 注意网站的反爬机制
import pymysql
import sys
import random
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait  # 等待对象
from selenium.webdriver.support import expected_conditions as EC  # 条件
from selenium.webdriver.common.by import By  # 定义定位器的常量

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


# 发送请求 获取数据
def get_content_by_selenium(url):  # 搜索页面结果加密使用此方法
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    driver.get(url=url)
    # 请求
    time.sleep(random.uniform(1, 2))
    res = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div[1]/div')))
    html_str = driver.page_source

    return html_str


def get_html(url):
    # 构建请求头，伪装成浏览器
    db_headers = {'User-Agent': random.choice(agent_list), 'referer': 'https://book.douban.com/'}
    basic_url = url
    db_novel = requests.get(url=basic_url, headers=db_headers)
    db_novel_html = db_novel.text
    return db_novel_html


# 获取图书标签
def parse_html_tag(db_html):
    db_html = etree.HTML(db_html)
    book_tag = db_html.xpath('//div[@class="indent tag_cloud"]//td/a/text()')
    book_tag = list(book_tag)[:20]  # 设置获取标签的数量
    return book_tag


# 定义函数：解析数据（提取需要的数据）
def parse_html_book(db_html):
    # 将text数据转换成html数据
    db_html = etree.HTML(db_html)
    # 使用xpath提取相关数据
    # 作者  （译者） 出版社   时间   价格
    basic_info = db_html.xpath('//ul[@class="subject-list"]/li/div[@class="info"]/div[@class="pub"]/text()')
    basic_info = [info.replace("\n", "").strip().split("/") for info in basic_info]

    # 评价星级  评价人数
    rating_stars_class = db_html.xpath(
        '//ul[@class="subject-list"]/li/div[@class="info"]/div[@class="star clearfix"]/span[1]/@class')
    for i in range(len(rating_stars_class)):
        if rating_stars_class[i] == 'pl':
            rating_stars_class[i] = '00'

    rating_stars_class = [re.findall(r"\d+", star) for star in rating_stars_class]
    rating_stars_class = [str(info).replace("'", "") for info in rating_stars_class]
    rating_stars_class = [str(info).replace("[", "") for info in rating_stars_class]
    rating_stars_class = [str(info).replace("]", "") for info in rating_stars_class]

    rating_stars = db_html.xpath(
        '//ul[@class="subject-list"]/li/div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')

    rating_nums = db_html.xpath(
        '//ul[@class="subject-list"]/li/div[@class="info"]/div[@class="star clearfix"]/span[@class="pl"]/text()')
    rating_nums = [info.replace("\n", "").strip().split("/") for info in rating_nums]
    rating_nums = [str(info).replace("'", "") for info in rating_nums]
    rating_nums = [str(info).replace("[", "") for info in rating_nums]
    rating_nums = [str(info).replace("]", "") for info in rating_nums]
    # 获取书籍名称
    book_name = db_html.xpath('//ul[@class="subject-list"]//a/@title')

    # 获取书籍封面
    book_img = db_html.xpath('//*[@id="subject_list"]/ul//div[1]/a/img/@src')
    book_img = [str(info).replace("'", "") for info in book_img]

    # 获取书籍ID
    id_string = db_html.xpath('//*[@id="subject_list"]/ul//div[1]/a/@href')
    book_id = [re.findall(r"\d+", id) for id in id_string]
    book_id = [str(info).replace("'", "") for info in book_id]
    book_id = [str(info).replace("[", "") for info in book_id]
    book_id = [str(info).replace("]", "") for info in book_id]

    return basic_info, rating_stars, book_id, rating_nums, book_img, book_name, rating_stars_class


# 豆瓣未录入作者，随机生成n位数id
def parse_html_no_author(id_len):
    all_id = '0123456789'
    last_pos = len(all_id) - 1
    author_id = ''
    for _ in range(id_len):  # 随机生成n位id
        index = random.randint(0, last_pos)
        author_id = author_id + all_id[index]
    return author_id


# 作者id获取不到，a标签链接指向一个搜索页面的情况下,且能够搜索到作者时调用此函数
def parse_html_search_author(db_html):
    db_html = etree.HTML(db_html)
    id_string = db_html.xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div/div/div[1]/a/@href')
    author_id = [re.findall(r"\d+", str(id_string))]
    author_id = str(author_id).replace("'", "")
    author_id = str(author_id).replace("[", "")
    author_id = str(author_id).replace("]", "")
    i = len(author_id)
    if i >= 8:
        author_id = parse_html_no_author(9)
        # 7位数是作者id，8位数是图书id，所以选择生成九位随机数避免相同
    return author_id

# 作者信息
def parse_html_author(db_html):
    db_html = etree.HTML(db_html)
    # 获取到作者id
    id_string = db_html.xpath('//*[@id="info"]/span[1]/a/@href')
    author_id = [re.findall(r"\d+", str(id_string))]
    i = len(str(author_id))
    if i > 20:
        search_name = db_html.xpath('//*[@id="info"]/span[1]/a/text()')
        search_name = [info.replace("'", "") for info in search_name]
        author_url_1 = 'https://book.douban.com/subject_search?search_text={}'.format(search_name)

        author_url_1 = get_content_by_selenium(author_url_1)
        author_id = parse_html_search_author(author_url_1)
    if i < 5:
        id_string = db_html.xpath('//*[@id="info"]/a/@href')
        author_id = [re.findall(r"\d+", str(id_string[0]))]
    author_id = str(author_id).replace("[", "")
    author_id = str(author_id).replace("]", "")
    author_id = str(author_id).replace("'", "")
    # 获取书籍简介和作者简介
    book_dec = db_html.xpath('//*[@id="link-report"]//div/div/p/text()')
    str_desc = ''
    for desc in book_dec:
        str_desc = str_desc + desc
    book_str_desc = str(str_desc).replace("'", "")

    # 当简介太短的时候  没有all hidden这个span标签  直接跳过span标签查询div标签
    author_dec = db_html.xpath('//*[@id="content"]/div/div[1]/div[3]/div[@class="indent "]//div/p/text()')
    author_str_dec = str(author_dec).replace("'", "")
    return author_id, author_str_dec, book_str_desc


# 作者图片
def parse_html_aimg(db_html):
    db_html = etree.HTML(db_html)
    author_img = db_html.xpath('//*[@id="headline"]//div/img/@src')

    author_img = [str(info).replace("'", "") for info in author_img]
    author_img = [str(info).replace("[", "") for info in author_img]
    author_img = [str(info).replace("]", "") for info in author_img]
    return author_img


# 获取图书标签 豆瓣读书标签tag没有相关的id展示在网页端
tag_url = "https://book.douban.com/tag/?view=cloud"
tag_html = get_html(tag_url)
book_tag = parse_html_tag(tag_html)

time.sleep(random.uniform(0.5, 1.5))

# 连接数据库
conn = pymysql.connect(host='127.0.0.1', user='root', password='root', port=3306, database='bookrec', charset='utf8')
cursor = conn.cursor()

# 爬取小说标签并存入数据库sort
sid = [1 + n for n in range(len(book_tag))]
for n in range(len(book_tag)):
    sql = "insert ignore into sort(sid,sname) values('%d','%s')" % (sid[n], book_tag[n])
    cursor.execute(sql)
    conn.commit()
# 获取多页数据

#将书籍信息存入数据库
for tag in book_tag:
    print(tag)
    sid_n = book_tag.index(tag) + 1
    if sid_n > 5:  # 控制从第几个标签开始爬取数据
        for page in range(80, 120, 20):
            print("正在获取", page, "页")
            basic_url = "https://book.douban.com/tag/{tag}?start={page}&type=T".format(tag=tag, page=page)
            basic_html = get_html(basic_url)
            basic_info, rating_stars, book_id, rating_nums, book_img, book_name, rating_stars_class = parse_html_book(
                basic_html)
            index_none = 0
            for i in range(20):
                if rating_stars_class[i] == '00':
                    index_none = i
                    rating_stars[index_none:index_none] = ['0.0']

            time.sleep(random.uniform(1, 2.5))
            # 防反爬虫
            print("正在抓取图书信息")
            for id in book_id:
                id = id.replace("'", "")
                n = book_id.index(id)
                book_url = "https://book.douban.com/subject/{}/".format(id)
                book_html = get_html(book_url)
                authorID, author_dec, book_dec = parse_html_author(book_html)
                if authorID == id:
                    authorID = parse_html_no_author(9)
                author_dec = str(author_dec)
                book_dec = str(book_dec)
                if len(author_dec) < 10:
                    author_dec = '该作家暂无介绍'
                if len(book_dec) < 10:
                    book_dec = '该书籍暂无介绍'
                time.sleep(random.uniform(0.5, 1.5))
                if len(authorID) > 8:
                    author_img = 'https://img3.doubanio.com/f/book/0e27fcad0e64da9769f748b2070a295b56405077/pics/book/author-default-large.png'
                if len(authorID) <= 7:
                    author_url = "https://book.douban.com/author/{}/".format(authorID)
                    author_html = get_html(author_url)
                    author_img = parse_html_aimg(author_html)
                    if len(author_img) < 5:
                        author_img = 'https://img3.doubanio.com/f/book/0e27fcad0e64da9769f748b2070a295b56405077/pics/book/author-default-large.png'
                print("正在抓取作者信息")
                basic_info_len = len(basic_info[n])
                price_n = basic_info_len - 1
                publisher_n = basic_info_len - 3
                time_n = basic_info_len - 2
                for i in range(basic_info_len):
                    basic_info[n][i] = str(basic_info[n][i]).replace("'", "").strip()
                    basic_info[n][i] = str(basic_info[n][i]).replace("[", "")
                    basic_info[n][i] = str(basic_info[n][i]).replace("]", "")

                # author_sql = "insert ignore into author(aid,aname,adesc,aimg) values(%s,%s,%s,%s)" , (authorID, basic_info[n][0], str(author_dec), author_img)
                cursor.execute("insert ignore into author(aid,aname,adesc,aimg) values(%s,%s,%s,%s)",
                               (authorID, basic_info[n][0], author_dec, author_img))
                print("正在插入作者信息", n)
                # book_sql = "insert ignore into book(bid,bname,bimg,aid,bprice,bdesc,bpublisher,btime,sid,bstar,bnum) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" , (book_id[n], book_name[n], book_img[n], authorID, basic_info[n][basic_info_len-1], str(book_dec), basic_info[n][basic_info_len-3],basic_info[n][basic_info_len-2],sid[sid_n], rating_stars[n], rating_nums[n])
                cursor.execute(
                    "insert ignore into book(bid,bname,bimg,aid,bprice,bdesc,bpublisher,btime,sid,bstar,bnum) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (id, book_name[n], book_img[n], authorID, basic_info[n][price_n], book_dec,
                     basic_info[n][publisher_n], basic_info[n][time_n], sid_n, rating_stars[n], rating_nums[n]))
                print("正在插入书籍信息", n)

            time.sleep(random.uniform(1, 1.5))
            conn.commit()

    time.sleep(random.uniform(1, 1.5))
time.sleep(random.uniform(1, 1.5))


cursor.close()
conn.close()
