from flask import Flask, url_for, render_template, request, session, flash, redirect, jsonify
from flask_caching import Cache

import controller as pt

app = Flask(__name__)
app.config.from_envvar('SETTINGS')

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
    return render_template("index.html", data=data)


@app.route("/admin",methods=['GET'])
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
        flash("Please use HH:MM AM/PM or +59 format")
    return admin()




@app.route('/setup', methods=['POST'])
def do_setup():
    data_file = url_for('static', filename='data/setup.txt', _external=True)
    get = ["clac_method", "savings"]
    prayer.save_data(request.form.get, get, 'data/setup.txt', False)
    prayer.change_setup(*(prayer.read_data(data_file)))
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
