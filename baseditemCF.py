from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
import np
import pandas as pd

# 定义数据集，  注意这里采用字典存放数据，实际情况中数据是非常稀疏的， 很少有情况是现在这样
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

# 计算物品的相似矩阵
similarity_matrix = pd.DataFrame(np.zeros((len(items),len(items))),index=['A','B','C','D','E'],columns=['A','B','C','D','E'])

for itemID in items:
    for otheritemID in items:
        vec_item = []
        vec_otheritem=[]
        if itemID != otheritemID:# 物品与其它物品
            for userID in users:  #遍历物品——用户评分数据
                userRatings = users[userID] # itemRatings也是个字典  每条数据为所有用户对当前物品的评分
                if itemID in userRatings and otheritemID in userRatings: # 说明两个用户都对该物品评过分
                    vec_item.append(userRatings[itemID]) # 此处是此物品的评分中该用户的评分插入到list当中
                    vec_otheritem.append(userRatings[otheritemID])# 此处是将另外物品的评分中该用户的评分插入到list当中
                    # 这里可以获得相似性矩阵(共现矩阵)
                    # np.corrcoef 能够计算两个矩阵的相似矩阵 通过[0][1]将物品1和物品2的相似性获取出来并赋值给similarity_matrix这个5*5的空表当中
                    similarity_matrix[itemID][otheritemID] = np.corrcoef(np.array(vec_item),np.array(vec_otheritem))[0][1]

# 计算与物品5相似的前n个物品
n = 2
# ascending属性表示是否按升序排除，True是升序，False是降序
# 相似矩阵已经计算出每个物品之间的相似性，所以只需要将相似性降序，获取到前n个物品即可
similarity_items = similarity_matrix['E'].sort_values(ascending=False)[:n].index.tolist()
# 计算最终得分
# 计算物品E已经评分的平均值
base_score = np.mean(np.array([value for value in items['E'].values()]))
weighted_scores = 0.
corr_values_sum = 0.
for item in similarity_items:
    corr_value = similarity_matrix['E'][item]  # 物品E 和另外两个物品之间的相似性
    mean_item_score = np.mean(np.array([value for value in items[item].values()])) # 每个用户的打分平均值
    weighted_scores += corr_value * (users[1][item] - mean_item_score) # 加权分数    相似性*(分数-平均分数)
    corr_values_sum += corr_value   # 相似性相加
final_scores = base_score + weighted_scores/corr_values_sum # 最终打分 = 物品打分评分值 + 加权分数/总相似性

user_df.loc[1]['E'] = final_scores
print(user_df)