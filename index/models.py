from django.db import models
from django.utils import timezone
from user.models import User


# Create your models here.

# 书本分类
class Sort(models.Model):
    sid = models.CharField(primary_key=True, max_length=20)
    sname = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sort'


# 书本
class Book(models.Model):
    bid = models.CharField(primary_key=True, max_length=20)
    bstar = models.CharField(max_length=20, blank=True, null=True)
    bimg = models.CharField(max_length=100, blank=True, null=True)
    bname = models.CharField(max_length=20, blank=True, null=True)
    bpublisher = models.CharField(max_length=20, blank=True, null=True)
    btime = models.CharField(max_length=20, blank=True, null=True)
    sid = models.ForeignKey('Sort', models.DO_NOTHING, db_column='sid')
    bprice = models.CharField(max_length=20, blank=True, null=True)
    aid = models.ForeignKey('Author', models.DO_NOTHING, db_column='aid')
    bdesc = models.CharField(max_length=2000, blank=True, null=True)
    bnum = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book'


# 作者
class Author(models.Model):
    aid = models.CharField(primary_key=True, max_length=32)
    aimg = models.CharField(max_length=500, blank=True, null=True)
    aname = models.CharField(max_length=32, blank=True, null=True)
    adesc = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'author'

# 评论
class Comment(models.Model):
    cid = models.CharField(primary_key=True, max_length=20)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid')
    bid = models.ForeignKey('Book', models.DO_NOTHING, db_column='bid')
    cstar = models.CharField(max_length=20, blank=True, null=True)
    cdesc = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'

# 用户
class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=20)  # 用户id
    uemail = models.CharField(max_length=20, blank=True, null=True)  # 邮箱
    usex = models.CharField(max_length=20, blank=True, null=True)  # 性别
    uname = models.CharField(max_length=20, blank=True, null=True)  # 昵称
    upsw = models.CharField(max_length=100, blank=True, null=True)  # 密码
    uphone = models.CharField(max_length=20, blank=True, null=True)  # 手机号
    uadmin = models.IntegerField(blank=True, null=True)  # 是否管理员

    class Meta:
        managed = False
        db_table = 'user'

    @property
    def password(self):
        raise AttributeError('Can not read password！')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)  # 转变成hash加密

# 书单
class Cart(models.Model):
    db_table = 'cart'
    cid = models.AutoField(primary_key=True)          # id
    user = models.ForeignKey(User,related_name='user_cat', on_delete=models.CASCADE)  # 外键 用户
    book = models.ForeignKey(Book,related_name='book_cat', on_delete=models.CASCADE)     # 外键 商品
    pnum = models.IntegerField()                         # 数量
    sumprice = models.CharField(max_length=64)           # 总价格
                                                            #时间
    time = models.DateField(auto_now_add=True) # 创造时间

# 付款
class PayCart(models.Model):
    db_table = 'paycart'
    id = models.AutoField(primary_key=True)          # id
    cart = models.ForeignKey(Cart,related_name='carttopay', on_delete=models.CASCADE)  # 外键 用户

# 订单
class MyOrder(models.Model):
    order_id = models.AutoField(primary_key=True)  # 订单id
    user = models.ForeignKey(User, related_name='user_order', on_delete=models.CASCADE)  # 外键
    book = models.ForeignKey(Book, related_name='book_order', on_delete=models.CASCADE)  # 外键 商品
    allprice = models.FloatField()  # 总价
    paydate = models.DateTimeField  # 日期
    db_table = 'myorder'
    
    class Meta:
        db_table = 'index_myorder'