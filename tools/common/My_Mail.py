import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = 'root@mail.cxbdzd.com'  # 发件人邮箱账号
my_pass = 'A*s551789'  # 发件人邮箱密码


class My_Mail:
    def __init__(self):
        #self.server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        self.server = smtplib.SMTP("mail.cxbdzd.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25

    def send_mail(self,reciever, title,content,reciever_name ='reciever'):
        ret = True
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["FromServer", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([reciever_name, reciever])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = title  # 邮件的主题，也可以说是标题
        #self.server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        self.server.sendmail(my_sender, [reciever, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        #try:
        #    self.server.quit()  # 关闭连接
        #except Exception:
        #    ret = False
        return ret


if __name__ == '__main__':
    reciever_test = '835046414@qq.com'  # 收件人邮箱账号
    mail = My_Mail()
    ret = mail.send_mail(reciever_test,"title",'content','蓉儿')
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")

