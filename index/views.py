import random
from django.shortcuts import render,redirect,HttpResponse
from user.user_method import UserMethod
from .models import Book,Sort,Comment,Cart,PayCart,Author,MyOrder
from user.views import login_required,random_id
from user.models import User
from django.http import  HttpResponseRedirect,JsonResponse
from user.models import Address
import re
from .recommend import recommend_user
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import datetime as dt

# Create your views here.
def index(request):
    thisuser = UserMethod(request)
    userinfo = thisuser.getUserInfo()
    # [a, b] ~ [0, 12+4]
    # [a, c] ~ [0, 12+8]
    a = random.randrange(12)
    b = a+4
    c = a+8
    book1s = Book.objects.filter(sid=1).order_by("bnum").defer("bdesc")[a:b]
    #
    book2s = Book.objects.filter(sid=2).order_by("bnum").defer("bdesc")[a:b]
    #
    book3s = Book.objects.filter(sid=3).order_by("bnum").defer("bdesc")[a:b]
    #
    book4s = Book.objects.filter(sid=4).order_by("bnum").defer("bdesc")[a:b]
    #
    book5s = Book.objects.filter(sid=5).order_by("bnum").defer("bdesc")[a:b]
    #
    book6s = Book.objects.filter(sid=6).order_by("bnum").defer("bdesc")[a:b]

    #猜你喜欢
    bookrecs = Book.objects.order_by("bnum").defer("bdesc")[0:50]#销量前50
    if userinfo['islogin']:
        uid = userinfo['uid']
        user_com = Comment.objects.filter(uid=uid).first()
        if user_com != None:# 根据用户历史评价推荐
            bookid_rec = recommend_user(uid)
            print("\n")
            print("根据相似度计算推荐给用户的图书为：")
            for book in bookid_rec:
                print(book,end=", ")
            print("\n")
            bookrecs = Book.objects.filter(bid__in=bookid_rec).defer("bdesc")

            bookrecs = bookrecs[a:b]
        else:
            user = User.objects.filter(uid=userinfo['uid'])[0]
            if len(user.favor)>0:# 用户无历史评价，根据用户注册时选择的喜好推荐
                category = list(map(lambda x:int(x), user.favor))
                bookrecs = Book.objects.filter(sid__in=category).order_by("bnum").defer("bdesc")# 用户喜好分类的书籍按照销量排序
            bookrecs = bookrecs[a:b]
    else:
        bookrecs = bookrecs[a:b]

    author_id = random.randrange(671)
    authors = Author.objects.all()
    author = authors[author_id]
    aid = author.aid
    book_author = Book.objects.filter(aid=aid).defer("bdesc")[0:4]

    book_new = Book.objects.order_by("btime")[a:c]
    book_hot = Book.objects.order_by("-bnum")[a:c]
    book_high_score = Book.objects.filter(bnum__gt=100).order_by("-bstar")[a:c]
    data = {
        'userinfo': userinfo,
        'book1s': book1s,
        'book2s': book2s,
        'book3s': book3s,
        'book4s': book4s,
        'book5s': book5s,
        'book6s': book6s,
        'author':author,
        'book_author':book_author,
        'book_new':book_new,
        'book_rec':bookrecs,
        'book_hot':book_hot,
        'book_high_score':book_high_score
    }
    return render(request, "index.html", data)

# 书本详情
def bookdetail(request):
    thisuser = UserMethod(request)
    userinfo = thisuser.getUserInfo()
    bid = request.GET.get('bid')

    book = Book.objects.filter(bid=bid).first()
    sort = Sort.objects.filter(sid=book.sid).first()
    image = book.bimg
    price_string = book.bprice
    price  = [re.findall(r'\d+(?:\.\d+)?', str(price_string))]
    price = str(price).replace("[", "")
    price = str(price).replace("]", "")
    price = str(price).replace("'", "")
    price = float(price)
    unames_1 = unames_2 = []
    stars_1 = stars_2 = []

    comments = Comment.objects.filter(bid=bid)
    for comment in comments:
        user = User.objects.filter(uid=comment.uid.uid).first()
        unames_1.append(user.uname)
        star = int(comment.cstar) * 2

        stars_1.append(star)
    unames_2 = list(reversed(unames_1))
    stars_2 = list(reversed(stars_1))

    books = Book.objects.filter(sid=book.sid)[0:3]
    bought = False
    if userinfo and userinfo.get("uid") is not None:
        bought = MyOrder.objects.filter(user_id=userinfo["uid"], book_id=bid).exists()
    data={
        'userinfo':userinfo,
        'book':book,
        'sort':sort,
        'image':image,
        'price':price,
        'books':books,
        'comments':comments,
        'uname':unames_2,
        'star':stars_2,
        "bought":bought,
    }
    return render(request,"detail.html",data)

# 添加到书单
@login_required
def addtocart(request):
    thisuser = UserMethod(request)
    userinfo = thisuser.getUserInfo()
    thisuser = User.objects.filter(uid=userinfo['uid']).first()
    if request.method == 'POST':
        book_bid = request.POST.get('book_bid')
        userinfo_id = thisuser.uid
        pnum = request.POST.get('pnum')
        sumprice = request.POST.get('sumprice')
        thiscart = Cart.objects.filter(book_id=book_bid,user_id=userinfo_id).all()
        if len(thiscart) == 0:
            newcart = Cart(book_id=book_bid,user_id=userinfo_id,pnum=pnum,sumprice=sumprice)
            newcart.save()
        allcart = Cart.objects.filter(user_id=userinfo_id).count()
        return JsonResponse({
            'recode':1,
            'rmsg':'添加成功',
            'data':{
                'error':'',
                'allcart':allcart
            }
        })
    if request.method == 'GET':
        return HttpResponseRedirect("/showcart/")

# 获取书单数量
def getcartnum(request):
    if request.method == "GET":
        thisuser = UserMethod(request)
        userinfo = thisuser.getUserInfo()
        allcart = Cart.objects.filter(user_id=userinfo['uid']).count()
    return JsonResponse({
        'recode':1,
        'rmsg': '获取成功',
        'data':{
            'error':'',
            'allcart':allcart
        }
    })

# 展示书单
@login_required
def showcart(request):
    thisuser = UserMethod(request)
    userinfo = thisuser.getUserInfo()
    allcart = Cart.objects.filter(user_id=userinfo['uid']).all()
    allcartnum = Cart.objects.filter(user_id=userinfo['uid']).count()
    data = {
        'userinfo':userinfo,
        'allcartnum':allcartnum,
        'allcart':allcart
    }
    # 只能借三本书
    ordersNotFinished = MyOrder.objects.filter(user_id=userinfo['uid'], returndate=None)
    data['unreturnNum']=len(ordersNotFinished)
    data['cantBorrow']=1 if len(ordersNotFinished)>=3 else 0

    # 押金, 余额
    thisuser = User.objects.filter(uid=userinfo['uid']).first()
    data['deposit'] = 0 if thisuser.udeposit is None else thisuser.udeposit
    data['balance'] = 0 if thisuser.ubalance is None else thisuser.ubalance
        
    return render(request,'ShowCart.html',data)

#修改天数
def modify_books(request):
    if request.method == "POST":
        userinfo = UserMethod(request).getUserInfo()
        userinfo_id = userinfo['uid']
        book_id = request.POST.get('book_id')
        dayNum = request.POST.get("dayNum")
        data = {}
        cart = Cart.objects.filter(user_id=userinfo_id,book_id=book_id).first()
        if cart:
            oldPnum = cart.pnum
            cart.pnum = int(dayNum)
            sumprice = round(float(cart.sumprice) / oldPnum * cart.pnum, 2)
            # 总价超过书价
            if sumprice>cart.book.bookprice:
                data["error"] = "overprice"
                data["oldDayNum"] = int(oldPnum)
            else:
                cart.sumprice = sumprice
                cart.save()
            data['msg'] = '请求成功'
            return JsonResponse(data)

# 添加天数
def add_books(request):
    if request.method =="POST":
        userinfo = UserMethod(request).getUserInfo()
        userinfo_id = userinfo['uid']
        book_id = request.POST.get('book_id')
        data = {}
        cart = Cart.objects.filter(user_id=userinfo_id,book_id=book_id).first()
        if cart:
            sumprice = round(float(cart.sumprice) / cart.pnum * (cart.pnum + 1 ),2)
            # 总价超过书价
            if sumprice>cart.book.bookprice:
                data["error"] = "overprice"
                data["oldDayNum"] = cart.pnum
            else:
                cart.sumprice = sumprice
                cart.pnum += 1
                cart.save()

            data['msg'] = '请求成功'
            return JsonResponse(data)

# 删除天数
def sub_books(request):
    if request.method =="POST":
        userinfo = UserMethod(request).getUserInfo()
        userinfo_id = userinfo['uid']
        book_id = request.POST.get('book_id')
        data = {}
        cart = Cart.objects.filter(user_id=userinfo_id,book_id=book_id).first()
        if cart:
            if cart.pnum == 1:
                data['msg'] = '最少买一个'
            else:
                sumprice = round(float(cart.sumprice) / cart.pnum *(cart.pnum - 1 ),2)
                # 总价超过书价
                if sumprice<0:
                    data["error"] = "overprice"
                    data["oldDayNum"] = cart.pnum
                else:
                    cart.sumprice = sumprice
                    cart.pnum -=1
                    cart.save()
                data['msg'] = '请求成功'
                return JsonResponse(data)
        else:
            data['msg'] = '请添加商品'
            return  JsonResponse(data)

# 减少数目
def delcart(request):
    if request.method == 'GET':
        userinfo = UserMethod(request).getUserInfo()
        userinfo_id = userinfo['uid']
        book_id = request.GET.get('bid')
        Cart.objects.filter(user_id=userinfo_id,book_id=book_id).delete()
    return HttpResponseRedirect("/index/showcart")

# 支付
def cash_payment(request):
    if request.method == 'POST':
        allcartpay = PayCart.objects.filter().all()
        if allcartpay != '':
            PayCart.objects.filter().all().delete()
        userinfo = UserMethod(request).getUserInfo()
        userinfo_id = userinfo['uid']
        
        cartlist = request.POST.get("cartlist")
        cartlist = cartlist.split('#')
        for list in cartlist:
            if list != '':
                list = int(list)
                newcart = Cart.objects.filter(cid=list).first()
                cartpay = PayCart(cart_id=newcart.cid)
                cartpay.save()
        allcart = Cart.objects.filter(user_id=userinfo_id).all()
        user = User.objects.filter(uid=userinfo_id).first()
        for item in allcart:
            if str(item.cid) not in cartlist:
                continue
            book = Book.objects.filter(bid=item.book.bid).first()
            if book.bremain <=0:#库存不够
                continue
            book.bremain -= 1
            book.bnum += 1
            order = MyOrder(user_id=userinfo_id,book_id=item.book.bid,allprice=item.book.bprice*item.pnum, daynum=item.pnum, paydate=datetime.now())
            user.ubalance -= item.book.bprice*item.pnum
            item.delete()
            order.save()
            book.save()
        user.save()
    return HttpResponseRedirect("/index/showcart")

# 评论
@login_required
def comment(request):
    thisuser = UserMethod(request)
    userinfo = thisuser.getUserInfo()
    this_user = User.objects.filter(uid=userinfo['uid']).first()

    if request.method == 'POST':
        book_id = request.POST.get('id')
        this_book = Book.objects.filter(bid=book_id).first()
        comment_star = request.POST.get('comment_star')
        comment_desc = request.POST.get('comment')
        if comment_desc == '':
            msg = '留言不能为空！'
            return JsonResponse({
                'code': 0,
                'msg': msg,
                'data': {
                    'error': 1,
                }
            })
        else:
            comment_id = random_id(6)
            Comment(cid=comment_id,bid=this_book,uid_id=this_user.uid,cdesc=comment_desc,cstar=comment_star).save()
            this_book.bstar = "%.2f" % (eval(this_book.bstar) + eval(comment_star) * 2.0 / this_book.bnum)
            return JsonResponse({
                'code':1,
                'msg':'添加成功',
                'data': {
                'error': 0,
                }
            })

    return JsonResponse({
                'code':0,
                'msg':'添加失败',
                'data': {
                    'error': 1,
                }
            })
def search(request):
    userinfo = UserMethod(request).getUserInfo()
    search_text = request.GET.get('search')
    books_search = Book.objects.filter(bname__contains=search_text)
    data = {
        'userinfo': userinfo,
        'books': books_search,

    }

    return render(request,"list.html",data)

def sort_all(request):
    userinfo = UserMethod(request).getUserInfo()
    sid = eval(request.GET.get('sid'))
    sortType = eval(request.GET.get('sortType'))
    page = request.GET.get('page')
    #根据排序类型不同，来获取书籍列表
    if sid==0:
        if sortType==1:#根据借阅量排序（受欢迎程度）
            books = Book.objects.order_by("-bnum")
        elif sortType==2:#根据评价排序
            books = Book.objects.filter(bnum__gt=100).order_by("-bstar")
    else:
        books = Book.objects.filter(sid=sid)    
        if sortType==1:
            books = books.order_by("-bnum")
        elif sortType==2:
            books = books.filter(bnum__gt=100).order_by("-bstar")    
    pageSize = 10
    paginator = Paginator(books, pageSize)
    total_page = paginator.count
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)

    data = {
        'userinfo': userinfo,
        'books': book_list,
        'pages':total_page,
        'sid':sid,
        'sortType':sortType
    }
    return render(request,'list.html',data)

@login_required
def borrowHistory(request):
    userinfo = UserMethod(request).getUserInfo()
    #获取该用户所有借阅历史
    orders = list(MyOrder.objects.filter(user_id=userinfo["uid"]).all())
    unreturns = []#保存未还的记录
    returns = []#保存已还的记录
    now = datetime.now()
    for order in orders:
        #计算到期时间
        deadline = order.paydate+dt.timedelta(days=order.daynum)
        order.remainTime = deadline - now
        if order.returndate is None:
            unreturns.append(order)
        else:
            returns.append(order)
    #按照剩余到期时间排序
    unreturns = sorted(unreturns, key = lambda order:order.remainTime.microseconds, reverse=True)
    #按照借阅时间排序
    returns = sorted(returns, key = lambda order:order.paydate.timestamp(), reverse=True)
    #合并，未还在前，已还在前
    unreturns.extend(returns)

    data = {"orders":unreturns}
    error =  request.GET.get("error")
    if error and error == "nomoney":
        data['error'] = "余额不足！请充值"
    return render(request,'borrowHistory.html', data)

# 还书
@login_required
def returnBook(request):
    userinfo = UserMethod(request).getUserInfo()
    oid = request.GET['oid']
    order = MyOrder.objects.filter(order_id=oid).first()
    order.returndate = datetime.now()
    diff = order.returndate-order.paydate
    diffDays = diff.days-order.daynum
    order.extraprice = 0

    #超出天数，从余额扣费
    if diffDays>0:
        extraprice = diffDays*order.book.bprice
        if order.allprice + extraprice >= order.book.bookprice:#超时费用加上借书时的费用已经足够买下这本书了
            extraprice = order.book.bookprice - order.allprice #因为这本书卖给读者了，所以额外费用就是书的价格减去借书时的付款
        else:
            order.book.bremain += 1
            order.book.save()
        order.extraprice = extraprice
        user = User.objects.filter(uid=order.user.uid).first()
        user.ubalance -= order.extraprice
        user.save()
    else:
        order.book.bremain += 1
        order.book.save()
    order.save()
    return HttpResponseRedirect("/index/borrowed/")

@login_required
def buyBook(request):
    userinfo = UserMethod(request).getUserInfo()
    oid = request.GET['oid']
    user = User.objects.filter(uid=userinfo["uid"]).first()

    order = MyOrder.objects.filter(order_id=oid).first()
    diffPrice = order.book.bookprice - order.allprice
    if user.ubalance < diffPrice:
        return HttpResponseRedirect("/index/borrowed/?error=nomoney")
    else:
        order.returndate = datetime.now()
        user.ubalance -= diffPrice
        user.save()
        order.save()
    return HttpResponseRedirect("/index/borrowed/")


def authorDetail(request):
    aid = request.GET['aid']
    author = Author.objects.filter(aid=aid)[0]
    book_author = Book.objects.filter(aid=aid).defer("bdesc")[0:4]
    data = {'author':author,
        'book_author':book_author}
    return render(request,'authorDetail.html', data)


from .autoNotify import sendEmails
def sent_deadline_email(request):
    sendEmails()
    return JsonResponse({'status':'ok'})