from flask import render_template, url_for, flash, redirect, request
from starter import app, bcrypt, db
from starter.form import RegistrationForm, LoginForm
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

@app.route('/register', methods=["get", "post"])
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

@app.route('/login', methods=["get", "post"])
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


@app.route('/account')
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)
