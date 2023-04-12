import requests
from django.shortcuts import render, HttpResponse
from .models import User, Address, Editpwd
from .user_method import UserMethod
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from functools import wraps
import random
from werkzeug.security import generate_password_hash
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# Create your views here.

# 生成随机id
def random_id(id_len):
    all_id = '123456789'
    last_pos = len(all_id) - 1
    user_id = ''
    for _ in range(id_len):  # 随机生成n位id
        index = random.randint(0, last_pos)
        user_id = user_id + all_id[index]
    return user_id

def login_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        thisuser = UserMethod(request)
        userinfo = thisuser.getUserInfo()
        if userinfo['islogin'] is not True:
            return HttpResponseRedirect('/user/login/')
        return f(request, *args, **kwargs)
    return decorated_function
# 登陆
def login(request):
    if (request.method == 'POST'):
        username = request.POST.get('txtUsername')
        password = request.POST.get('txtPassword')
        # 查找用户
        u_phone =  User.objects.filter(Q(uphone=username))
        u_email = User.objects.filter(Q(uemail=username))
        u_name = User.objects.filter(Q(uname=username))
                    # | User.objects.filter(Q(uemail=username))
        # User.objects.filter(Q(uname=username)) |
        # 无用户
        if u_phone.count()|u_email.count()|u_name.count() == 0:
            context = {'error_name': 1, 'error_pwd': 0, 'username': username, 'userpwd': password}
            return render(request, 'login.html', context)
        else:
            # 验证密码
            if u_name.count()|u_email.count() ==0:
                thisuser = u_phone
                phone_login = True
            else :
                if u_phone.count()|u_name.count()==0:
                    thisuser = u_email
                    email_login = True
                else:
                    thisuser = u_name
                    name_login = True
            if User.verify_password(thisuser.first(),password):
                request.session['user'] = {'islogin': True,
                                           'username': thisuser.first().uname,
                                           'email': thisuser.first().uemail,
                                           'phone': thisuser.first().uphone,
                                           'sex': thisuser.first().usex,
                                           'uid':thisuser.first().uid,
                                           }
                request.session.set_expiry(1200)
                return HttpResponseRedirect("/index/")
            else:
                # 密码错误
                context = {'error_name': 0, 'error_pwd': 1, 'username': username, 'password': password}
                return render(request, 'login.html', context)
    else:
        # 通过get请求发送过来，就判断是否已经登陆
        this_user = UserMethod(request)
        userinfo = this_user.getUserInfo()

        if userinfo['islogin']:
            return HttpResponseRedirect("/index/")
        else:
            return render(request, 'login.html')

# 注册
def register(request):
    if request.method =="POST":
        username = request.POST.get('txt_username')
        phone = request.POST.get('txt_phone')
        password = request.POST.get('txt_password')
        email = request.POST.get('txt_email')
        uid = random_id(3)                          #生成3位ID与爬取的2位id区别开
        sex = request.POST.get('select_sex')
        request.session["user"] = {'islogin': True, 'username': username, 'email': email,'uid':uid,'phone': phone}
        password_hash = generate_password_hash(password)
        newuser = User(uname=username, uemail=email, upsw=password_hash,uphone=phone,usex=sex,uid=uid,uadmin=0)
        newuser.save()
        return HttpResponseRedirect('/user/login')
    return render(request,'register.html')

# 检测是否注册
def register_exist(request):
    phone = request.GET.get('phone')
    count = User.objects.filter(uphone=phone).count()
    return JsonResponse({'count': count})

# 退出登陆
def logout(request):
    thisuser = UserMethod(request)
    userinfo = thisuser.getUserInfo()
    if userinfo['islogin']:
        request.session.pop("user")  #清空session
        return HttpResponseRedirect("/index/")

# 个人主页
@login_required
def personalinfo(request):
    thisuser = UserMethod(request)
    userinfo = thisuser.getUserInfo()
    thisuser = User.objects.filter(uphone=userinfo['phone']).first()
    context = {'username':thisuser.uname,'email':thisuser.uemail,'sex':thisuser.usex,'thisuser':thisuser}
    return render(request,"personalinfo.html",context)

# 发送验证码邮件
def sent_email_captcha(email,random):
    my_sender = '54800204@qq.com'  # 发件人邮箱账号
    my_pass = 'jysiyopdxmxxbjid'  # 发件人邮箱密码
    my_user = email  # 收件人邮箱账号

    msg = MIMEText(random, 'plain', 'utf-8')
    msg['From'] = formataddr(["hariki", my_sender])
    msg['To'] = formataddr(["FK", my_user])
    msg['Subject'] = "验证码"

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    server.quit()

# 修改密码
@login_required
def editpassword(request):
    thisuser = UserMethod(request)
    userinfo = thisuser.getUserInfo()
    thisuser = User.objects.filter(uid=userinfo['uid']).first()

    captcha_radom = random_id(6)

    if request.method == 'POST':
        cpatcha = request.POST.get('captcha')
        newpassword = request.POST.get('newpassword')


        if Editpwd.objects.filter(captcha=cpatcha).count() :
            newpassword_hash = generate_password_hash(newpassword)
            thisuser.upsw = newpassword_hash
            thisuser.save()
            Editpwd.objects.filter(captcha=cpatcha).delete()

            return HttpResponseRedirect("/index/")
        else:
            context = {'error_pwd': 1, 'captcha': cpatcha, 'newpassword': newpassword ,'userinfo': userinfo }
            return render(request,'editpwd.html',context)
    else:
        context = {'error_pwd': 0, 'captcha': '', 'newpassword': '', 'userinfo': userinfo}
        sent_email_captcha(thisuser.uemail, captcha_radom)
        save_captcha = Editpwd(eid=random_id(3), email=thisuser.uemail, captcha=captcha_radom)
        save_captcha.save()
        return render(request,'editpwd.html',context)


@login_required
def editaddress(request):
    thisuser = UserMethod(request)
    user_info = thisuser.getUserInfo()
    userinfo1 = User.objects.filter(uid=user_info['uid']).first()
    this_address = Address.objects.filter(uid=userinfo1.uid)

    if this_address.count() == 0:
        addressinfo = {
            'userinfo':user_info,
            'address':{
                'curaddress':'请设置收货地址',
                'province':'湖北省',
                'city':'武汉市',
                'district':'江夏区',
                'detail':'',
                'getname':'',
                'getphone':'',
                'getcode':''
            }
        }
        if request.method == 'POST':
            province = request.POST.get('province')
            city = request.POST.get('city')
            district = request.POST.get('district')
            adddetail = request.POST.get('adddetail')
            getphone = request.POST.get('getphone')
            getcode = request.POST.get('getcode')
            getname = request.POST.get('getname')
            newaddress = Address(province=province, city=city, district=district,
                                 detail=adddetail, get_name=getname, get_phone=getphone,
                                 get_code=getcode,uid=userinfo1.uid)
            newaddress.save()
            return HttpResponseRedirect("/address")
    else:#数据库存有地址
        this_address = this_address.first()
        addressinfo = {
            'userinfo':user_info,
            'address':{
                'curaddress':this_address.getFullAddress(),
                'province':this_address.province,
                'city':this_address.city,
                'district':this_address.district,
                'detail':this_address.detail,
                'getname':this_address.get_name,
                'getphone':this_address.get_phone,
                'getcode':this_address.get_code
            }
        }
        if request.method =='POST':
            province = request.POST.get('province')
            city = request.POST.get('city')
            district = request.POST.get('district')
            adddetail = request.POST.get('adddetail')
            getphone = request.POST.get('getphone')
            getcode = request.POST.get('getcode')
            getname = request.POST.get('getname')
            this_address.province = province
            this_address.city =city
            this_address.district = district
            this_address.detail = adddetail
            this_address.get_name = getname
            this_address.get_phone = getphone
            this_address.get_code = getcode
            this_address.save()
            return HttpResponseRedirect("/address/")
    return render(request,"address.html",addressinfo)

@login_required
def getaddress(request):
    thisuser = UserMethod(request)
    user_info = thisuser.getUserInfo()
    usinfo1 = User.objects.filter(uid=user_info['uid']).first()
    this_address = Address.objects.filter(uid=usinfo1.uid)

    if this_address.count() == 0:
        return JsonResponse({
            'recode':0,
            'rmsg':'无地址',
            'data':{
                'error':'',
                'address':{
                    'province': '湖北省',
                    'city': '武汉市',
                    'district': '江夏区',
                    'detail': ''
                }
            }
        })
    else:
        thisaddress = this_address.first()
        return JsonResponse({
            'recode': 1,
            'rmsg': '获取地址成功',
            'data': {
                'error': '',
                'address': {
                    'province': thisaddress.province,
                    'city': thisaddress.city,
                    'district': thisaddress.district,
                    'detail': thisaddress.detail
                }
            }
        })