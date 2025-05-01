from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

# Настроим секретный ключ для работы сессий
app.secret_key = os.urandom(24)

app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():
    # Получаем URL изображения из сессии, если он есть
    image_url = session.get('image_url')

    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = url_for('static', filename=f'img/{filename}')

            # Сохраняем URL изображения в сессии
            session['image_url'] = image_url

        return redirect(url_for('index'))

    return render_template('index.html', image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)
