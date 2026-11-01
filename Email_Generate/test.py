from tools.custom_tools import *
#
# # tool = store_poesy_to_txt
tool = send_message
#
tool.run(file_path='poie.txt')
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
#
# #
# def send_email():
#     # 配置邮箱服务器信息
#     smtp_server = 'smtp.qq.com'
#     smtp_port = 465
#     # 配置发件人和收件人信息
#     sender = '934942965@qq.com'
#     receiver = 'lg11012309@163.com'
#     password = 'asdf110123'
#     # 创建 SMTP 对象
#     smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
#     # 登录邮箱
#     smtp.login(sender, password)
#     # 设置邮件内容
#     subject = 'Python 自动发送邮件测试'
#     body = '这是一封来自 Python 脚本的自动发送邮件。'
#     msg = MIMEText(body, 'plain', 'utf-8')
#     msg['From'] = Header(sender, 'utf-8')
#     msg['To'] = Header(receiver, 'utf-8')
#     msg['Subject'] = Header(subject, 'utf-8')
#     # 发送邮件
#     smtp.sendmail(sender, receiver, msg.as_string())
#     # 关闭连接
#     smtp.quit()
#
#
# if __name__ == '__main__':
#     send_email()