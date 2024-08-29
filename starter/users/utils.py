
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from starter import mail

def save_picture(form_picture):
    rand_hex = secrets.token_hex(8)
    _, f_exe = os.path.splitext(form_picture.filename)
    picture_fn = rand_hex + f_exe
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    ouput_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(ouput_size)
    
    i.save(picture_path)

    return picture_fn



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='fnegest75@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you didn't make this request just simply ignore it.
    '''
    mail.send(msg)