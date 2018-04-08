from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from os import urandom
from os import path, makedirs
from werkzeug.security import check_password_hash
import dbmake


app = Flask(__name__)
app.secret_key = urandom(26)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elephant.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
   if 'username' in session:
      username = session['username']
      return 'Logged in as ' + username + '<br>' + \
         "<b><a href = '/logout'>click here to log out</a></b>"
   return render_template('Index.html')


@app.route('/logout/')
def logout():
   session.pop('username', None)
   session.pop('_flashes', None)
   return redirect(url_for('index'))

@app.route('/login/', methods = ['GET', 'POST'])
def login():
   error = None
   
   if request.method == 'POST':
      usercorrect =  db.session.query(dbmake.Users).filter_by(username = request.form['username'] ).first()     
      if usercorrect == None : 
        flash ("Sorry! Username invalid !")
        return redirect(url_for('index'))

      
      enter = check_password_hash(usercorrect.password,request.form['password'])
      if enter == False  : 
          flash ("Sorry! Password incorrect!")
          return redirect(url_for('index'))
      
      else:

        session['username'] = request.form['username']
        return redirect(url_for('index'))

   return render_template('Login.html', error = error)


@app.route('/register/', methods = ['GET' , 'POST'])
def register(): 
  '''Registration form'''
  APP_ROOT = path.dirname(path.abspath(__file__))

  if request.method == 'POST': 
    new_user = dbmake.Users(username = request.form['username'] , password = request.form['password'])
    usercorrect = db.session.query(dbmake.Users).filter_by(username = new_user.username).first()
    
    if usercorrect == None : 
      
      target = path.join(APP_ROOT , 'ImageRepo/')
      target = path.join(target, request.form['username'])
      target = path.join(target,"DisplayPicture/")
      makedirs(target)
      

      db.session.add(new_user)
      db.session.commit()
      session['username'] = request.form['username']

      return redirect(url_for('add_details'))
    
    
    flash("Sorry! Username already exists !")
    return redirect(url_for('index'))

  return render_template('register.html')



 

@app.route('/adddetails/' , methods = ['GET' , 'POST'])
def add_details() : 
  ''' Fill up user details after registering '''

  if not hasattr(session, 'username'):
    return redirect(url_for('login'))

  APP_ROOT = path.dirname(path.abspath(__file__))
  if request.method == 'POST' :
    user_details = dbmake.UserData()
    target = path.join(APP_ROOT , 'ImageRepo/')
    target = path.join(target, session['username'])
    target = path.join(target,"DisplayPicture/")

    # if not path.exists(target) :
    #   makedirs(target)

    #destination = "/".join([target,"pp"])
    
    pp = request.files['file']
    pp.save(path.join(target,"pp"))

    ImageLocation = "ImageRepo/"+session['username']+"/DisplayPicture/pp.jpeg"
    print("!!!!!",ImageLocation)
    user_details.all_details(bio = request.form['bio'] , display_picture = ImageLocation)
    db.session.add(user_details)
    db.session.commit()
    return redirect(url_for('index'))


  return render_template('add_details.html')

if __name__ == "__main__" :
   app.run(debug = True)