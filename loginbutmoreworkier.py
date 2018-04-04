from flask import Flask, flash, redirect, render_template, request, url_for, session
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(26)

@app.route('/')
def index():
   if 'username' in session:
      username = session['username']
      return 'Logged in as ' + username + '<br>' + \
         "<b><a href = '/logout'>click here to log out</a></b>"
   return render_template('Index.html')


# @app.route('/')
# def index():
#    return render_template('Index.html')

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
   error = None
   
   if request.method == 'POST':
      if request.form['username'] != 'admin' or \
         request.form['password'] != 'admin':
         error = 'Invalid username or password. Please try again!'
      else:

        flash('You were successfully logged in')
        session['username'] = request.form['username']
        return redirect(url_for('index'))

   return render_template('Login.html', error = error)

if __name__ == "__main__" :
   app.run(debug = True)