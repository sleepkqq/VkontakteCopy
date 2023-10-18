import flickrapi
from flask import request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from app import app
from app.models import User, Image
from config import api_key, api_secret

flickr_admin = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
flickr_upload = flickrapi.FlickrAPI(api_key, api_secret, format='etree')


@app.route('/')
def main():
    return redirect(url_for('feed'))


@app.route('/feed')
def feed():
    return render_template('feed.html', current_user=current_user)


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            error_message = 'Пользователя с таким именем не существует' \
                if not user else 'Неправильный пароль'
            return jsonify({
                'success': False,
                'message': error_message
            })

        login_user(user)
        return jsonify({
            'success': True,
        })


@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    if request.method == 'POST':
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        username_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        if username_exists or email_exists:
            error_message = 'Данное имя пользователя уже используется' \
                if username_exists else 'Данная почта уже используется'
            return jsonify({
                'success': False,
                'message': error_message
            })

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        login_user(new_user)

        return jsonify({
            'success': True,
        })


@app.route('/authorization', methods=['GET'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    return render_template('authorization.html')


@login_required
@app.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({
            'success': True
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Войдите в аккаунт'
        })


@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return render_template('404page.html'), 404
    return render_template('profile.html', user=user)


@app.errorhandler(405)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404page.html'), 404


@login_required
@app.route('/image/upload', methods=['POST'])
def upload_photo():
    photo = request.files['photo']
    text = request.form.get('text')

    if photo:
        username = current_user.username
        filename = photo.filename
        response = flickr_upload.upload(filename=filename, fileobj=photo, title=text, description=username)
        photo_id = response.find('photoid').text

        sizes = flickr_admin.photos.getSizes(photo_id=photo_id)

        url = None

        for size in sizes['sizes']['size']:
            if size['label'] == 'Original':
                url = size['source']
                break

        new_image = Image(photo_id, url, username, text)
        new_image.save()

        return jsonify({
            'success': True,
            'message': 'Фото успешно загружено'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка'
        })


@login_required
@app.route('/image/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    image = Image.query.filter_by(id=image_id).first()
    if image:
        flickr_admin.photos.delete(photo_id=image.photo_id)
        image.remove()
        return jsonify({
            'success': True,
            'message': 'Фото успешно удалено'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка'
        })


@app.route('/images', methods=['GET'])
def photos_page():
    photos = Image.query.all()
    return render_template('images.html', photos=photos)
