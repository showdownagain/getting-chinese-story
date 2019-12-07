import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

ssl._create_default_https_context = ssl._create_unverified_context 

def sent_eml(txt_name):
    username = '******' #邮箱有户名
    password='********' #登录密钥，推荐使用QQ邮箱，网易邮箱的垃圾邮件阻止策略非常麻烦
    sender='*****@qq.com'
    receiver='*****@kindle.cn'
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message_docx = MIMEText(open(txt_name, 'rb').read(), 'base64', 'utf8')
    # 用add_header 方法可以避免附件中文编码的问题
    message_docx.add_header('content-disposition', 'attachment', filename=txt_name)
    message.attach(message_docx)
    message['Subject'] = 'convert'#确保kindle收到的邮件主题为convert这样才能自动转换
    try:
        smtpObj = smtplib.SMTP() 
    #连接到服务器
        smtpObj.connect('smtp.qq.com',25)
    #登录到服务器
        smtpObj.login(username,password) 
    #发送
        smtpObj.sendmail(sender,receiver,message.as_string()) 
    #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
