from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),                        # 主页
    path('detail/', views.bookdetail, name='detail'),           # 详细页面
    path('addtocart/', views.addtocart, name='addtocart'),      # 添加到书单
    path('getcartnum1/', views.getcartnum, name='getcartnum'),  # 添加到书单
    path('showcart/', views.showcart, name='showcart'),         # 展示书单
    path('modifybooks1/', views.modify_books, name='modifybooks'), # 修改借阅天数
    path('addbooks1/', views.add_books, name='addbooks'),       # 借阅天数+1
    path('subbooks1/', views.sub_books, name='subbooks'),       # 借阅天数-1
    path('deletcart/', views.delcart, name='deletcart'),        # 删除书单的商品
    path('cash_pay/', views.cash_payment, name='cash_pay'),     # 支付
    path('comment/',views.comment,name='comment'),              # 评论
    path('search/',views.search,name='search'),                 # 搜索
    path('sortall/',views.sort_all,name='sortall'),             # 排序
    path('borrowed/',views.borrowHistory,name='borrowed'),      # 借阅历史
    path('returnbook/',views.returnBook,name='returnbook'),     # 还书
    path('buybook/',views.buyBook,name='buybook'),              # 买书
    path('authordetail/',views.authorDetail,name='authordetail'), #作者详情
    path('sentdeadlines/', views.sent_deadline_email, name='sentdeadlines'), #发送归还邮件
]

app_name='index'
