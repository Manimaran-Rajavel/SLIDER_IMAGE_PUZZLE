from flask import Flask, render_template, request, redirect, url_for 
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static/images"


@app.route('/')
def index():
    image_folder = 'static/images'
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    return render_template('index.html', image_files=image_files)

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
    print(name)
    return render_template('game.html', name=name)


if __name__ == '__main__':
    app.run(debug=False)