import os
import smtplib
import threading
import urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings

from app.job.constants import EMAIL
from utils.logger.syslogger import SysLogger


class SendEmailClient(object):

    @classmethod
    def send_email_sync(cls, receivers=EMAIL.CHOICES_LIST, subject='神州网信招聘', content='个人简历', attachments=[]):
        threading.Thread(target=cls.send_email, args=(receivers, subject, content, attachments)).start()

    @classmethod
    def send_email(cls, receivers, subject, content, attachments):
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = settings.SEND_MAIL
        message['To'] = ','.join(receivers)

        message.attach(MIMEText(content, _subtype='html', _charset='utf-8'))

        if len(attachments) > 0:
            for index, attachment in enumerate(attachments):
                file_path = os.path.join(settings.MEDIA_ROOT, urllib.parse.unquote(attachment))
                filename = urllib.parse.unquote(attachment.split('_', 2)[-1])
                if not os.path.exists(file_path):
                    SysLogger.error(f"{filename} 文件不存在！")
                    continue
                att = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
                att.add_header('Content-Disposition', 'attachment', filename=filename)
                att.add_header('Content-Type', 'application/octet-stream')
                message.attach(att)
        try:
            smtp_obj = smtplib.SMTP(settings.MAIL_HOST, 587, timeout=10)
            smtp_obj.login(settings.SEND_MAIL, settings.MAIL_PWD)
            smtp_obj.sendmail(settings.SEND_MAIL, receivers, message.as_string())
            smtp_obj.quit()
        except smtplib.SMTPException as exp:
            SysLogger.error(exp)
        except Exception as exp:
            SysLogger.exception(exp)
