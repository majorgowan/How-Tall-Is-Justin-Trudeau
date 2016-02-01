# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = 'graphyDB.db'
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def split_list_string(comma_delimited):
    return [a.strip() for a in comma_delimited.split(',')]

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/how_tall_is')
def how_tall_is():
    return render_template('how_tall_is.html')

@app.route('/show_stats', methods=['POST'])
def show_stats():
    import urllib
    # get user ip address
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if user_ip is not None:
        user_location = urllib.urlopen('http://freegeoip.net/json/' + user_ip).read()
        #print('Your location is ' + user_location)
    else:
        user_city = None
    # survey results
    trudeau = int(request.form.get("trudeauHeightHidden"))
    obama = int(request.form.get("obamaHeightHidden"))
    user_height = int(request.form.get("userHeightHidden"))
    user_gender = request.form["gender"]
    # record results in database
    # check if ip is unique
    ip_list = g.db.execute('SELECT user_ip FROM heights').fetchall()
    if ip_list is not None:
        # ip_list is a list of 1-tuples, convert to list of strings
        ip_list = [a[0] for a in ip_list]
    # for testing purposes, don't use the ip address restriction
    ip_list = []
    if unicode(user_ip) in ip_list:
        flash('Your ip: ' + str(user_ip) + ' has already answered, you sneaky sod!!')
        answer_list = g.db.execute('SELECT * FROM heights WHERE user_ip=?', [user_ip]).fetchall()[0]
        answer_list = answer_list[1:]
    else:
        answer_list = [user_ip, trudeau, obama, \
                       user_height, user_gender, user_location]
        g.db.execute( \
            'INSERT INTO heights ' + \
            '    (user_ip, trudeau, obama, ' + \
                 'user_height, user_gender, user_location) ' + \
            'VALUES (?, ?, ?, ?, ?, ?)', \
            answer_list)
        g.db.commit()
        print(answer_list)
        flash('Your ip: ' + str(user_ip) + '. . . Thanks for your input you lovely sod!')
    return render_template('show_stats.html', answer_list=answer_list)

@app.route('/show_questionnaire_answers', methods=['GET','POST'])
def show_questionnaire_answers():
    # get user ip address
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # survey results
    trudeau = float(request.form['trudeau'])
    harper = float(request.form['harper'])
    obama = float(request.form['obama'])
    pizza = request.form.get('pizza')
    drink = request.form.get('drink')
    user_height = float(request.form['user_height'])
    user_shoe = int(request.form['user_shoe'])
    user_gender = request.form.get('user_gender')
    # record results in database
    # check if ip is unique
    ip_list = g.db.execute('SELECT user_ip FROM responses').fetchall()
    if ip_list is not None:
        # ip_list is a list of 1-tuples, convert to list of strings
        ip_list = [a[0] for a in ip_list]
    # for testing purposes, don't use the ip address restriction
    ip_list = []
    if unicode(user_ip) in ip_list:
        flash('Your ip: ' + str(user_ip) + ' has already answered, you sneaky sod!!')
        answer_list = g.db.execute('SELECT * FROM responses WHERE user_ip=?', [user_ip]).fetchall()[0]
        answer_list = answer_list[1:]
    else:
        answer_list = [user_ip, trudeau, harper, obama, pizza, drink, \
                       user_height, user_shoe, user_gender]
        g.db.execute( \
            'INSERT INTO responses ' + \
            '    (user_ip, trudeau, harper, obama, pizza, drink, ' + \
                 'user_height, user_shoe, user_gender) ' + \
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', \
            answer_list)
        g.db.commit()
        flash('Your ip: ' + str(user_ip) + '. . . Thanks for your input you lovely sod!')
    return render_template('show_questionnaire_answers.html', answer_list=answer_list)

#@app.route('/')
#def show_entries():
#    cur = g.db.execute('SELECT title, text FROM entries ORDER BY id DESC')
#    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
#    return render_template('show_entries.html', entries=entries)

#@app.route('/add', methods=['POST'])
#def add_entry():
#    if not session.get('logged_in'):
#        abort(401)
#    g.db.execute('INSERT INTO entries (title, text) VALUES (?, ?)', \
#            [request.form['title'], request.form['text']])
#    g.db.commit()
#    flash('New entry was successfully posted')
#    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()

