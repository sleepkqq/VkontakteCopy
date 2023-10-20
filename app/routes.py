import flickrapi
from flask import request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from app import app
from app.models import User, Image, save_edit
from config import api_key, api_secret
import re

flickr_admin = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
flickr_upload = flickrapi.FlickrAPI(api_key, api_secret, format='etree')


@app.route('/', methods=['GET'])
def main():
    return redirect(url_for('feed'))


@app.route('/feed', methods=['GET'])
def feed():
    return render_template('feed.html', current_user=current_user)


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({
            'success': False,
            'message': 'Вы уже авторизованы'
        })

    phone_number = request.json['phoneNumber']
    password = request.json['password']

    user = User.query.filter_by(phone_number=phone_number).first()

    if not user or not user.check_password(password):
        error_message = 'Пользователя с таким номером не существует' \
            if not user else 'Неправильный пароль'
        return jsonify({
            'success': False,
            'message': error_message
        })

    login_user(user)

    return jsonify({
        'success': True,
        'message': 'Авторизация прошла успешно'
    })


@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({
            'success': False,
            'message': 'Вы уже авторизованы'
        })

    phone_number = request.json['phoneNumber']
    pattern = r"^((\+7|7|8)([0-9]){10})$"
    if not re.match(pattern, phone_number):
        return jsonify({
            'success': False,
            'message': 'Номер не соответствует шаблону'
        })

    first_name = request.json['firstName']
    second_name = request.json['secondName']
    password = request.json['password']

    phone_number_exists = User.query.filter_by(phone_number=phone_number).first()

    if phone_number_exists:
        error_message = 'Данный номер уже используется'
        return jsonify({
            'success': False,
            'message': error_message
        })

    new_user = User(phone_number, first_name, second_name)
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
            'success': True,
            'message': 'Вы успешно вышли из аккаунта'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Войдите в аккаунт'
        })


@app.route('/<string:username>', methods=['GET'])
def user_profile(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return render_template('404page.html'), 404

    return render_template('profile.html', user=user)


@app.route('/edit/status/<string:username>', methods=['POST'])
def edit_user_status(username):
    if not current_user.is_authenticated or current_user.username != username:
        error_message = 'Авторизуйтесь' \
            if not current_user.is_authenticated else 'Это не ваш аккаунт'
        return jsonify({
            'success': False,
            'message': error_message
        })

    status = request.json['newStatus']
    if len(status) > 100:
        return jsonify({
            'success': False,
            'message': f'Ограничение 100 символов, у вас {len(status)}'
        })

    user = User.query.filter_by(username=username).first()
    user.status = status
    save_edit()

    return jsonify({
        'success': True,
        'message': 'Статус успешно изменён'
    })


@app.errorhandler(405)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404page.html'), 404


@app.route('/image/upload', methods=['POST'])
def upload_photo():
    if not current_user.is_authenticated:
        return jsonify({
            'success': False,
            'message': 'Авторизуйтесь'
        })

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


@app.route('/image/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    image = Image.query.filter_by(id=image_id).first()

    if not current_user.is_authenticated or current_user.username != image.username:
        error_message = 'Авторизуйтесь' \
            if not current_user.is_authenticated else 'Это не ваше фото'
        return jsonify({
            'success': False,
            'message': error_message
        })

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
