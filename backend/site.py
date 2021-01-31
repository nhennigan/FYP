from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def login_page():
   return render_template('login.html')

@app.route('/home/', methods = ['POST','GET'])
def home_page():
    return render_template('home.html')

@app.route('/admin_home/', methods = ['POST','GET'])
def admin_home_page():
    return render_template('admin_home.html')

@app.route('/lect_home/')
def lect_home_page():
    return render_template('lect_home.html')

@app.route('/calendarview/')
def calendar_page():
    return render_template('calendar.html')

@app.route('/mapview/')
def map_page():
    return render_template('map.html')

@app.route('/examofficeinfo/')
def info_page():
    return render_template('info.html')

if __name__ == '__main__':
   app.run(debug = True,host='0.0.0.0')
