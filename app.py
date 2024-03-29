import os

from flask import Flask, url_for, render_template, request, session, flash, redirect, jsonify
from flask_caching import Cache
from werkzeug.utils import secure_filename

import controller as pt

UPLOAD_FOLDER = './static/data'
app = Flask(__name__)
app.config.from_envvar('SETTINGS')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = b'_5#y2L"F4Q8z\n\xeec]/'
# Check Configuring Flask-Cache section for more details
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
prayer = pt.Prayer()


@app.route("/", methods=['GET', 'POST'])
def index():
    print('prayer Times for today in Eugene/Oregon\n' + ('=' * 41))
    data = prayer.map_prayer_data()
    if request.method == 'POST':
        return jsonify(data)
    return render_template("index.html", data=data, payload=prayer.read_data())


@app.route("/admin", methods=['GET'])
def admin():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return render_template("admin.html", data=prayer.timeNames, methods=prayer.get_calculation_methods(),
                               payload=prayer.read_data())


@app.route("/update_iqama", methods=['POST'])
def update_iqama():
    print('Iqama Changed')
    payload = [request.form.get(i) for i in prayer.timeNames]
    if prayer.validate(payload):
        prayer.update_data(payload, 'iqama')
        return redirect(url_for('index'))
    else:
        flash(u"Please use HH:MM AM/PM or +59 format", "update_iqama")
    return admin()


@app.route('/uploader', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return admin()
    else:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename("prayer_data.xlsx")))
        prayer.change_prayer_data()
        return redirect(url_for('index'))


@app.route('/update_setup', methods=['POST'])
def do_setup():
    prayer.update_data(request.form.get('clac_method'), 'calculation')
    prayer.update_data(float(request.form.get('latitude')), 'latitude')
    prayer.update_data(float(request.form.get('longitude')), 'longitude')
    prayer.update_data(int(request.form.get('time_zone')), 'time_zone')
    return redirect(url_for('index'))


@app.route('/change_header', methods=['POST'])
def do_header():
    prayer.update_data(request.form.get('header_1'), 'header_1')
    prayer.update_data(request.form.get('header_2'), 'header_2')
    prayer.update_data(request.form.get('header_3'), 'header_3')
    prayer.update_data(request.form.get('disable_api') == "on", 'read_from_file')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if request.method == 'GET':
        return redirect(url_for('admin'))
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong info!', category='login')
    return admin()


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
