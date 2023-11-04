from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.exc import IntegrityError
import os
from models import Users
from database import sessionlocal
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static/images"
app.config['SECRET_KEY'] = "0618"


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup_data', methods=['GET', 'POST'])
def signup_data():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        sessionDB = sessionlocal()
        existing_user = sessionDB.query(Users).filter_by(name=username).first()
        if existing_user:
            return render_template('signup.html', message="Username is already in use. Please choose another username.")
        
        hashed_password = generate_password_hash(password)
        
        new_user = Users(name=username, email=email, Password=hashed_password)
        
        sessionDB.add(new_user)
        sessionDB.commit()
        sessionDB.close()
        return redirect(url_for('login'))

@app.route('/login_access', methods=['GET', 'POST'])
def login_access():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        sessionDB = sessionlocal()
        user = sessionDB.query(Users).filter_by(name=username).first()

        if user and check_password_hash(user.Password, password):
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('index'))
        else:
            return "Invalid username or password. Please try again."

    return render_template('login.html')



@app.route('/home')
def index():
    image_folder = 'static/images'
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    return render_template('index.html', image_files=image_files, name=session.get('name'))

@app.route('/admin')
def admin():
    image_folder = 'static/images'
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    return render_template('admin.html', image_files=image_files)

@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        upload_image = request.files['image']

        if upload_image.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
            upload_image.save(filepath)
    return redirect(url_for('admin'))

@app.route('/delete/<filename>')
def delete_image(filename):
    print(filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(image_path):
        os.remove(image_path)

    return redirect(url_for('admin'))

@app.route('/game/<name>')
def game(name):
    return render_template('game.html', name=name)

@app.route('/progress/<int:seconds>')
def progress(seconds):
    user_id = session.get('user_id')
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    mins = f"{minutes}:{remaining_seconds}"

    sessionDB = sessionlocal()
    
    sessionDB.query(Users).filter(Users.id == user_id).update({'score':mins})
    sessionDB.commit()

    all_data = sessionDB.query(Users).all()

    return render_template('progress.html', all_data=all_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)