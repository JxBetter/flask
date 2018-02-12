from flask import render_template, current_app
from flask_mail import Message
from blog.app.factory import mail
from threading import Thread


def send_async_email(app, message):
    with app.app_context():
        mail.send(message)


def send_email(to, prefix, template, enable=False, **kwargs):
    if enable:
        app = current_app._get_current_object()
        message = Message(prefix, sender=app.config['MAIL_SENDER'], recipients=[to])
        message.body = render_template(template + '.txt', **kwargs)
        message.html = render_template(template + '.html', **kwargs)
        thr = Thread(target=send_async_email, args=[app, message])
        thr.start()
        return thr
