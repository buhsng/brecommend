from datetime import datetime
import threading
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from index.models import MyOrder

class EmailSender:
    def __init__(self, email, authcode):
        self.email = email
        self.autocode = authcode
        self.server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        
    def login(self):
        self.server.login(self.email, self.autocode)
        
    def quit(self):
        self.server.quit()
        
    def sendEmail(self, toEmail, msg):
        msg = MIMEText(msg, 'plain', 'utf-8')
        msg['From'] = formataddr(["hariki", self.email])
        msg['To'] = formataddr(["FK", toEmail])
        msg['Subject'] = "重理工图书馆, 还书通知"
        self.server.sendmail(self.email, [toEmail, ], msg.as_string())

def getNearDeadlines():
    orders = MyOrder.objects.filter(returndate=None).all()
    result = {}
    now = datetime.now()
    for order in orders:
        diff = now-order.paydate
        remainDays = order.daynum - diff.days
        if remainDays<=3:
            email = order.user.uemail
            if result.get(email) is None:
                result[email] = {}
            result[email][order.book.bname] = remainDays
    return result

def generateEmailMsg(deadlines):
    msg = '''来自重庆理工大学图书馆的通知：您借阅的以下书籍即将到期或已过期：'''
    result = {}
    for email in deadlines:
        ls = []
        for book in deadlines[email]:
            remainDays = deadlines[email][book]
            if remainDays<0:
                ls.append(book+'已过期'+str(remainDays)+'天')
            else:
                ls.append(book+'剩余'+str(remainDays)+'天')
        result[email] = msg+'、'.join(ls)+'。'
    return result
    
def sendEmails():
    sender = EmailSender('2324489588@qq.com', 'qwxeevwnrgaadhhc')
    sender.login()
    emailDict = generateEmailMsg(getNearDeadlines())
    for email in emailDict:
        sender.sendEmail(email, emailDict[email])
    sender.quit()
    
        