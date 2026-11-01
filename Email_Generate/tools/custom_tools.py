from crewai.tools import tool
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@tool("将文本写入文档中")
def store_poesy_to_txt(content: str) -> str:
    """
    将编辑后的书信文本内容自动保存到txt文档中
    """
    try:
        filename = "/Users/ligang/PycharmProjects/LLM/Agents/Email_Generate/poie.txt"
        # 将文本写入txt文档中
        with open(filename, 'w') as file:
            file.write(content)

        # 返回结果展示：文件已经写入
        return f"File written to {filename}."
    except Exception:
        return "Error with the input for the tool."



@tool("发送文本到邮件")
def send_message():
    '''
    读取生成的本地书信文件txt文本,并以邮件的形式发送到某个人的邮箱中
    '''

    # 邮箱配置
    sender_email = "934942965@qq.com"  # 你的QQ邮箱地址
    sender_password = "hvibxvycjlapbbih"  # 你的QQ邮箱SMTP授权码
    receiver_email = "lg11012309@163.com"  # 收件人邮箱地址

    # 邮件内容
    subject = "❤️"
    with open('/Users/ligang/PycharmProjects/LLM/Agents/Email_Generate/poie.txt') as fw:
        body = fw.read()
    # 设置邮件内容
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # 连接到SMTP服务器并发送邮件
    try:
        # QQ 邮箱的 SMTP 服务器地址
        smtp_server = "smtp.qq.com"
        smtp_port = 465  # 使用 SSL 加密

        # 建立与 SMTP 服务器的连接
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.connect(smtp_server, smtp_port)
        server.login(sender_email, sender_password)

        # 发送邮件
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("邮件发送成功!")

    except Exception as e:
        print(f"邮件发送失败: {e}")

    finally:
        server.quit()
