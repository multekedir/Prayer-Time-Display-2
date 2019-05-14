from flask import Flask, url_for, render_template, request, session, abort, flash, redirect, json, jsonify
from threading import Thread, Event
from time import sleep
import Prayer as pt
import os
from flask_caching import Cache

app = Flask(__name__)
app.config['DEBUG'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xeec]/'
# Check Configuring Flask-Cache section for more details
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
prayer = pt.Prayer()


@app.route("/", methods=['GET', 'POST'])
def index():
    data_file = url_for('static', filename='data/setup.txt', _external=True)
    iqama_file = url_for('static', filename='data/iqama.txt', _external=True)
    print('prayer Times for today in Eugene/Oregon\n' + ('=' * 41))
    if not prayer.is_setup:
        session['logged_in'] = False
        prayer.setup(data_file, iqama_file)
    data = prayer.map_prayerdata()
    if request.method == 'POST':
        return jsonify(data)
    return render_template("index.html", data=data)


@app.route("/admin")
def admin():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        print(prayer.get_difference())
        return render_template("admin.html", data=prayer.timeNames, methods=prayer.get_claculation_methods(),
                               defVals=prayer.get_difference())


@app.route("/admin", methods=['POST'])
def admin_post():
    where = 'data/iqama.txt'
    data_file = url_for('static', filename=where, _external=True)
    print("Saving to = ", data_file)
    if not prayer.save_data(request.form.get, prayer.timeNames, where, True):
        flash("Please use HH:MM AM/PM or +59 format")
    else:
        prayer.set_iqama(data_file)
        return redirect(url_for('index'))
    return admin()


@app.route('/setup', methods=['POST'])
def do_setup():
    data_file = url_for('static', filename='data/setup.txt', _external=True)
    get = ["clac_method", "savings"]
    prayer.save_data(request.form.get, get, 'data/setup.txt', False)
    prayer.change_setup(*(prayer.read_data(data_file)))
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def do_admin_login():
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
