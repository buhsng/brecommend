from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
import np
import pandas as pd
# a = [1,0,0,0]
# b = [1,0.5,0.5,0]
# # c = cosine_similarity([a,b])
# # print(c[0])
# c = pearsonr(a,b)
# print(c)

# users = np.array([[5,3,4,4],[3,1,2,3],[4,3,4,3],[3,3,1,5],[1,5,5,2]])
# a_1_1 = cosine_similarity(users)
# print(a_1_1)
#
# a_1_2 = np.corrcoef(users)
# print(a_1_2)

# 定义数据集， 也就是那个表格， 注意这里我们采用字典存放数据， 因为实际情况中数据是非常稀疏的， 很少有情况是现在这样
def loadData():
    items={'A': {1: 5, 2: 3, 3: 4, 4: 3, 5: 1},
           'B': {1: 3, 2: 1, 3: 3, 4: 3, 5: 5},
           'C': {1: 4, 2: 2, 3: 4, 4: 1, 5: 5},
           'D': {1: 4, 2: 3, 3: 3, 4: 5, 5: 2},
           'E': {2: 3, 3: 5, 4: 4, 5: 1}
          }
    users={1: {'A': 5, 'B': 3, 'C': 4, 'D': 4},
           2: {'A': 3, 'B': 1, 'C': 2, 'D': 3, 'E': 3},
           3: {'A': 4, 'B': 3, 'C': 4, 'D': 3, 'E': 5},
           4: {'A': 3, 'B': 3, 'C': 1, 'D': 5, 'E': 4},
           5: {'A': 1, 'B': 5, 'C': 5, 'D': 2, 'E': 1}
          }
    return items,users
# 定义物品和用户字典使其不仅能够通过用户找到对物品的评分，也能通过物品找到用户对其的评分
items, users = loadData()
# pandas.DataFrame().T 表示对此表的转置(线性代数)
item_df = pd.DataFrame(items).T
user_df = pd.DataFrame(users).T
# 此处生成一个空的5*5的表
similarity_matrix = pd.DataFrame(np.zeros((len(users),len(users))),index=[1,2,3,4,5],columns=[1,2,3,4,5])
# 遍历每条用户-物品评分数据
for userID in users:
    for otheruserID in users:
        vec_user = []
        vec_otheruser=[]
        if userID != otheruserID:# 用户与其它用户
            for itemID in items:  #遍历物品——用户评分数据
                itemRatings = items[itemID] # itemRatings也是个字典  每条数据为所有用户对当前物品的评分
                if userID in itemRatings and otheruserID in itemRatings: # 说明两个用户都对该物品评过分
                    vec_user.append(itemRatings[userID]) # 此处是将用户对某个物品的评分插入到list当中
                    vec_otheruser.append(itemRatings[otheruserID])# 此处是将另外的用户对同一个物品的评价插入到list当中
                    # 这里可以获得相似性矩阵(共现矩阵)
                    # np.corrcoef 能够计算两个矩阵的相似矩阵 通过[0][1]将用户1和用户2的相似性获取出来并赋值给similarity_matrix这个5*5的空表当中
                    similarity_matrix[userID][otheruserID] = np.corrcoef(np.array(vec_user),np.array(vec_otheruser))[0][1]
# 计算前n个相似的用户
n = 2
# ascending属性表示是否按升序排除，True是升序，False是降序
# 相似矩阵已经计算出每个用户之间的相似性，所以只需要将相似性降序，获取到前n个用户即可
similarity_users = similarity_matrix[1].sort_values(ascending=False)[:n].index.tolist()
# 计算最终得分
# 计算user1 已经评分的平均值
base_score = np.mean(np.array([value for value in users[1].values()]))
weighted_scores = 0.
corr_values_sum = 0.
for user in similarity_users:
    corr_value = similarity_matrix[1][user]  # user1 和另外两个用户之间的相似性
    mean_user_score = np.mean(np.array([value for value in users[user].values()])) # 每个用户的打分平均值
    weighted_scores += corr_value * (users[user]['E'] - mean_user_score) # 加权分数    相似性*(分数-平均分数)
    corr_values_sum += corr_value   # 相似性相加
final_scores = base_score + weighted_scores/corr_values_sum # 最终打分 = 用户打分评分值 + 加权分数/总相似性

user_df.loc[1]['E'] = final_scores
print(user_df)
