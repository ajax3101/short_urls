from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_bcrypt import bcrypt
from models import User, Link, Log  # Импортируем модель пользователя из файла models.py
from forms import RegisterForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Секретный ключ для защиты сессий

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Функция для загрузки пользователя по id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Хешируем пароль перед сохранением в базу данных
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Создаем нового пользователя и сохраняем его в базе данных
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно! Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы!', 'success')
    return redirect(url_for('index'))

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(characters, k=6))
    # Проверяем, существует ли уже ссылка с таким кодом
    while Link.query.filter_by(keyword=short_url).first() is not None:
        short_url = ''.join(random.choices(characters, k=6))
    return short_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_link():
    original_url = request.form['url']
    title = request.form['title']
    # Генерируем уникальный код для сокращенной ссылки
    keyword = generate_short_url()

    # Создаем новую запись в базе данных
    new_link = Link(keyword=keyword, url=original_url, title=title)
    db.session.add(new_link)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/<string:keyword>')
def redirect_to_original(keyword):
    # Ищем сокращенную ссылку в базе данных
    link = Link.query.filter_by(keyword=keyword).first()
    if link:
        return redirect(link.url)
    else:
        return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)

