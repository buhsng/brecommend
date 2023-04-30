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
        self.server.sendmail(self.email, [toEmail, ], msg.as_string())
        
    def sendEmails(self, toEmails, msg):
        self.server.sendmail(self.email, toEmails, msg.as_string())

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
    
def sendEmails(emailSender):
    emailDict = generateEmailMsg(getNearDeadlines())
    for email in emailDict:
        emailSender.sendEmail(email, emailDict[email])

if __name__=="__main__":
    sender = EmailSender('2324489588@qq.com', 'qwxeevwnrgaadhhc')
    sender.login()
    sendEmails(sender)
    sender.quit()
    
        