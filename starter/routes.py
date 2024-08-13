import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from starter import app, bcrypt, db
from starter.form import RegistrationForm, LoginForm, UpdadteAccountForm
from starter.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        "author": "Jane Doe",
        "title": "The Art of Coding",
        "content": "Coding is both a science and an art. It requires creativity and logical thinking to build efficient solutions.",
        "date_posted": "2024-08-01"
    },
    {
        "author": "John Smith",
        "title": "Exploring Machine Learning",
        "content": "Machine learning is transforming industries with its ability to learn from data. Understanding its fundamentals is crucial for leveraging its full potential.",
        "date_posted": "2024-08-02"
    },
    {
        "author": "Alice Johnson",
        "title": "Adventures in Web Development",
        "content": "Web development continues to evolve with new technologies and frameworks. Staying updated with the latest trends is key to building modern web applications.",
        "date_posted": "2024-08-03"
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You can now login", "success")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home')) 

def save_picture(form_picture):
    rand_hex = secrets.token_hex(8)
    _, f_exe = os.path.splitext(form_picture.filename)
    picture_fn = rand_hex + f_exe
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    ouput_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(ouput_size)
    
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdadteAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', 
                           title='Account', 
                           image_file=image_file,
                           form=form)
