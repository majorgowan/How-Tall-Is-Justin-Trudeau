# all the imports
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'graphyDB.db')
#DATABASE = 'graphyDB.db'
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

@app.route('/how_tall_is')
def how_tall_is():
    return render_template('how_tall_is.html')

@app.route('/how_tall_is_graph_stats', methods=['POST'])
def how_tall_is_graph_stats():
    import urllib
    # get user ip address
    # from http://stackoverflow.com/questions/22868900/ ...
    #                    how-do-i-safely-get-the-users-real-ip-address-in-flask-using-mod-wsgi
    trusted_proxies = {'127.0.0.1', '127.7.30.1'}  # define your own set
    # trusted_proxies = []
    route = request.access_route + [request.remote_addr]
    remote_addr = next((addr for addr in reversed(route) 
                              if addr not in trusted_proxies), request.remote_addr)
    user_ip = remote_addr
    # get user location
    user_location = urllib.urlopen('http://freegeoip.net/json/' + user_ip).read()
    # survey results
    trudeau = int(request.form.get("trudeauHeightHidden"))
    user_height = int(request.form.get("userHeightHidden"))
    user_gender = request.form["gender"]
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
        answer_list = [user_ip, trudeau, \
                       user_height, user_gender, user_location]
        # record results in database
        g.db.execute( \
            'INSERT INTO heights ' + \
            '    (user_ip, trudeau, ' + \
                 'user_height, user_gender, user_location) ' + \
            'VALUES (?, ?, ?, ?, ?)', \
            answer_list)
        g.db.commit()
        print(answer_list)
        flash('Your ip: ' + str(user_ip) + '. . . Thanks for your input you lovely sod!')
    # query database to get lists of all responses
    female_data = g.db.execute('SELECT trudeau, user_height FROM heights WHERE user_gender=?', \
                               ['female']).fetchall()
    male_data = g.db.execute('SELECT trudeau, user_height FROM heights WHERE user_gender=?', \
                               ['male']).fetchall()
    neither_data = g.db.execute('SELECT trudeau, user_height FROM heights WHERE user_gender=?', \
                               ['neither']).fetchall()
    female_trudeau = [a[0] for a in female_data]
    female_user = [a[1] for a in female_data]
    male_trudeau = [a[0] for a in male_data]
    male_user = [a[1] for a in male_data]
    neither_trudeau = [a[0] for a in neither_data]
    neither_user = [a[1] for a in neither_data]

    return render_template('how_tall_is_graph_stats.html', \
            male_trudeau=male_trudeau, male_user=male_user, \
            female_trudeau=female_trudeau, female_user=female_user, \
            neither_trudeau=neither_trudeau, neither_user=neither_user, \
            user_gender=user_gender, user_height=user_height, trudeau=trudeau)

if __name__ == '__main__':
    app.run()

