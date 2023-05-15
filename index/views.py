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

# Create your views here.
def index(request):
    thisuser = UserMethod(request)
    userinfo = thisuser.getUserInfo()
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
        'book_rec':bookrecs
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

# 添加书本
def add_books(request):
    if request.method =="POST":
        userinfo = UserMethod(request).getUserInfo()
        userinfo_id = userinfo['uid']
        book_id = request.POST.get('book_id')
        data = {}
        cart = Cart.objects.filter(user_id=userinfo_id,book_id=book_id).first()
        if cart:
            cart.sumprice = round(float(cart.sumprice) / cart.pnum * (cart.pnum + 1 ),2)
            cart.pnum += 1
            cart.save()

            data['msg'] = '请求成功'
            return JsonResponse(data)

# 删除书本
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
                cart.sumprice = round(float(cart.sumprice) / cart.pnum *(cart.pnum - 1 ),2)
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
            book = Book.objects.filter(bid=item.book.bid).first()
            if book.bremain <=0:#库存不够
                continue
            book.bremain -= 1
            book.save()
            order = MyOrder(user_id=userinfo_id,book_id=item.book.bid,allprice=eval(item.book.bprice)*item.pnum, daynum=item.pnum, paydate=datetime.now())
            user.ubalance -= eval(item.book.bprice)*item.pnum
            order.save()
        user.save()
        allcart.delete()
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
            context ={
                'bid':book_id
            }
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
    sid = request.GET.get('sid')
    page = request.GET.get('page')
    books = Book.objects.filter(sid=sid)
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
        'sid':sid
    }
    return render(request,'list.html',data)

@login_required
def borrowHistory(request):
    userinfo = UserMethod(request).getUserInfo()
    orders = list(MyOrder.objects.filter(user_id=userinfo["uid"]).all())
    orders = sorted(orders, key = lambda order:order.paydate.timestamp(), reverse=True)
    data = {"orders":list(orders)}
    return render(request,'borrowHistory.html', data)

@login_required
def returnBook(request):
    userinfo = UserMethod(request).getUserInfo()
    bid = request.GET['bid']
    order = MyOrder.objects.filter(user_id=userinfo['uid'], book_id=bid).first()
    order.book.bremain += 1
    order.book.save()
    order.returndate = datetime.now()
    diff = order.returndate-order.paydate
    diffDays = diff.days-order.daynum
    order.extraprice = 0
    #超出天数，从余额扣费
    if diffDays>0:
        order.extraprice = diffDays*order.book.bprice
        order.user.balance -= order.extraprice
        order.user.save()
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