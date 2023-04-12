# import pymysql
# import re

# conn = pymysql.connect(host='127.0.0.1', user='root', password='miku233..', port=3306, database='bookrec', charset='utf8')
# # cursor = conn.cursor()
# #
# # sql = "SELECT bnum,bid FROM book"
# # cursor.execute(sql)
# # num_all = cursor.fetchall()
# # # 更新书本的评价人数
# # for obj in num_all:
# #     bid_str = str(obj[1])
# #     obj_str = str(obj[0]).replace("(", "")
# #     obj_str = str(obj_str).replace(")", "")
# #     obj_str = re.findall(r"\d+", obj_str)
# #     sql_update = "update book set bnum= '{}' where bid='{}'".format(obj_str[0],bid_str)
# #     cursor.execute(sql_update)
# #     conn.commit()
# #
# # cursor.close()
# # conn.close()

from scipy.stats import pearsonr
import numpy as np
import pandas as pd
items = np.array([[3,5,2,4],[1,2,1,2],[2,3,4,3],[3,1,3,5],[3,2,5,1]])
cols = ['item'+str(i) for i in range(1,6)]
a = pd.DataFrame(np.corrcoef(items),columns = cols,index=cols)

print(a)