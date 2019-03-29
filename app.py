from flask import Flask, url_for, render_template, request, session, abort, flash, redirect, json,jsonify
from threading import Thread, Event
from time import sleep
import Prayer as pt
import os
from collections import OrderedDict
#from flask_socketio import SocketIO, emit


app = Flask(__name__)
#socketio = SocketIO(app)
app.config['DEBUG'] = True

# thread = Thread()
# thread_stop_event = Event()
#
# class PrayerThread(Thread):
#     def __init__(self):
#         self.delay = 1
#         super(PrayerThread, self).__init__()
#
#     def prayertimeGenerator(self):
#         """
#         Generate a random number every 1 second and emit to a socketio instance (broadcast)
#         Ideally to be run in a separate thread?
#         """
#         #infinite loop of magical random numbers
#         print("Making random numbers")
#         while not thread_stop_event.isSet():
#             data = pt.map_prayerdata()
#             print("prayertimeGenerator =", data)
#             socketio.emit('newdata', {'data': data}, namespace='/prayers')
#             sleep(self.delay)
#
#     def run(self):
#         self.prayertimeGenerator()

@app.route("/")
def index():
    print('Prayer Times for today in Eugene/Oregon\n' + ('=' * 41))
    # prayTimes.setMethod('ISNA')
    # times = prayTimes.getTimes(date.today(), (, ), -8, dst=1);
    # for i in ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Midnight']:
    #     print(i + ': ' + times[i.lower()])
    data = pt.map_prayerdata(url_for('static', filename='iqama.txt', _external=True))
    return render_template("index.html", data=data)

@app.route("/admin")
def admin():
    if not session.get('logged_in'):
        return render_template("login.html" )
    else:
        return render_template("admin.html", data=pt.timeNames)

@app.route("/admin", methods=['POST'])
def admin_post():
    data_file = url_for('static', filename='iqama.txt', _external=True)
    print("Reading from = ", pt.read_data(data_file))
    if(not pt.save_data(request.form.get,pt.timeNames)):
        flash("Please use HH:MM AM/PM or +59 format")
    else:
        pt.map_prayerdata(data_file)

        return redirect(url_for('index'))
    return admin()



@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong info!', category='login')
    return admin()

@app.route('/get', methods=['POST'])
def get_data():
    # data = json.loads(, object_pairs_hook=OrderedDict)
    send = jsonify(pt.map_prayerdata(url_for('static', filename='iqama.txt', _external=True)))
    print("sending =", send)

    return send

# @socketio.on('connect', namespace='/prayers')
# def test_connect():
#     # need visibility of the global thread object
#     global thread
#     print('Client connected')
#
#     #Start the random number generator thread only if the thread has not been started before.
#     if not thread.isAlive():
#         print("Starting Thread")
#         thread = PrayerThread()
#         thread.start()
#
# @socketio.on('disconnect', namespace='/prayers')
# def test_disconnect():
#     print('Client disconnected')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run()
#     socketio.run(app)
