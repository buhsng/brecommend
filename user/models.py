from django.db import models
from werkzeug.security import generate_password_hash, check_password_hash


# Create your models here.

class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=20)  # 用户id
    uemail = models.CharField(max_length=20, blank=True, null=True)  # 邮箱
    usex = models.CharField(max_length=20, blank=True, null=True)  # 性别
    uname = models.CharField(max_length=20, blank=True, null=True)  # 昵称
    upsw = models.CharField(max_length=300, blank=True, null=True)  # 密码
    uphone = models.CharField(max_length=20, blank=True, null=True)  # 手机号
    uadmin = models.IntegerField(blank=True, null=True)  # 是否管理员

    @property
    def password(self):
        raise AttributeError('Can not read password！')

    @password.setter
    def password(self, password):
        self.upsw = generate_password_hash(password)  # 转变成hash加密

    # 举例：
    # pbkdf2: sha256:150000$WlU6hKVc$b85531b52dafbead09b983cd6942840ded3fd897bde528531c677cc95046c52e
    # 编码方法，pbkdf2: sha256
    # 盐值，WlU6hKVc
    # 迭代次数，150000
    # 哈希编码，b85531b52dafbead09b983cd6942840ded3fd897bde528531c677cc95046c52e
    def verify_password(self, password):
        if self == None:
            return False
        return check_password_hash(self.upsw, password)  # 验证密码


    class Meta:
        managed = False
        db_table = 'user'

class Address(models.Model):
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', primary_key=True)  # 用户id
    province = models.CharField(max_length=30, blank=True, null=True)  # 省份
    city = models.CharField(max_length=30, blank=True, null=True)  # 城市
    district = models.CharField(max_length=30, blank=True, null=True)  # 县区
    detail = models.CharField(max_length=128, blank=True, null=True)  # 详细地区
    get_name = models.CharField(max_length=128, blank=True, null=True)
    get_phone = models.CharField(max_length=128, blank=True, null=True)
    get_code = models.CharField(max_length=128, blank=True, null=True)

    def getFullAddress(self):
        return self.province + ' ' + self.city + ' ' + self.district + ' ' + self.detail + '(' + self.get_name + '收)' + ' ' + self.get_phone

    class Meta:
        managed = False
        db_table = 'address'

class Editpwd(models.Model):
    eid = models.CharField(primary_key=True, max_length=20)
    email = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    captcha = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editpwd'
