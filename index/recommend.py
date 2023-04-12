import pymysql
from math import sqrt


def recommend_user(id):
    # 将获取数据的方式放在此处才会刷新一次就获取一次数据
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, database='bookrec',
                           charset='utf8')
    cursor = conn.cursor()

    sql_user = "SELECT uid,bid,cstar FROM comment"
    users = {}
    items = {}
    cursor.execute(sql_user)
    user_all = cursor.fetchall()

    for user in user_all:
        if user[0] not in users:
            users[user[0]] = {}
        users[user[0]][user[1]] = float(user[2])

    for item in user_all:
        if item[1] not in items:
            items[item[1]] = {}
        items[item[1]][item[0]] = float(item[2])



    bookid_list = []
    r = recommender(users)
    k = r.recommends(id)
    for i in range(len(k)):
        bookid_list.append(k[i][0])

    # 关闭数据库
    cursor.close()
    conn.close()
    return bookid_list

class recommender:
    # data:数据集
    # k : 得出最相近k的近邻
    # metric ： 使用的计算相似的的方法
    # n : 推荐的个数
    def __init__(self, data, k=3, metric='pearson', n=15):
        self.k = k
        self.n = n
        self.user_id_2 = {}
        self.user_id_3 = {}
        self.book_id_2 = {}

        self.metric = metric

        if self.metric == 'pearson':
            self.fn = self.pearson
        if type(data).__name__ == 'dict':
            self.data = data

    def conver_book_id_2(self, id):
        if id in self.book_id_2:
            return self.book_id_2[id]
        else:
            return id
        
    #皮尔逊相关稀疏计算公式
    def pearson(self,rating1,rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x,2)
                sum_y2 += pow(y,2)
        if n == 0:
            return 0

        denominator = sqrt(sum_x2 - pow(sum_x,2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator ==0:
            return 0
        else:
            return (sum_xy-(sum_x * sum_y) / n) / denominator

    #计算用户之间的相似度
    def nearest_user(self,userid):
        distances = []
        for instance in self.data:
            if instance != userid:# 不是同一个id
                distance = self.fn(self.data[userid],self.data[instance])
                distances.append((instance,distance))
        # 排序
        distances.sort(key=lambda artistTuple: artistTuple[1],reverse=True)
        return distances

    def recommends(self,user):
        recommendations = {}

        nearest = self.nearest_user(user)
        userRatings = self.data[user]
        totalRatings = 0.0
        #总评分
        for i in range(self.k):
            totalRatings += nearest[i][1]
        if totalRatings == 0.0:
            totalRatings = 1.0

        for i in range(self.k):
            weight = nearest[i][1] / totalRatings
            uid = nearest[i][0]
            neighborRatings = self.data[uid]#uid用户所有的评分
            for bid in neighborRatings:
                if bid not in userRatings:
                    recommendations[bid] = (neighborRatings[bid] * weight)
                else:
                    if bid not in recommendations:
                        recommendations[bid] = (neighborRatings[bid] * weight)
                    recommendations[bid] = (recommendations[bid] + neighborRatings[bid] * weight)

        recommendations = list(recommendations.items())
        #将推荐书籍和相似度转换成字典
        recommendations = [(self.conver_book_id_2(k),v)for(k,v) in recommendations]
        #排序
        recommendations.sort(key=lambda artisTuple:artisTuple[1],reverse= True)
        i = 0
        for k,v in recommendations:
            i = i+1
            print("书籍：",k , end=" ")
            print("相似度:",v, end=", ")
            if i%4 == 0:
                print("\n")
        return recommendations[:self.n]
