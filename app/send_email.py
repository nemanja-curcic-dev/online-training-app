from flask_mail import Message
from threading import Thread
from flask import current_app, render_template
from app import mail


def send_asynchronous(msg, app):
    with app.app_context():
        mail.send(msg)


def send_mail(sender, subject, to, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(sender=sender, subject=subject, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_asynchronous, args=[msg, app])
    thread.start()
    return thread