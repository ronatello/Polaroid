from flask import Flask, flash, redirect, render_template, request, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import urandom
from os import path, makedirs
from werkzeug.security import check_password_hash
import itertools
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
   return render_template('Login.html')


@app.route('/logout/')
def logout():
   session.pop('username', None)
   session.pop('_flashes', None)
   return redirect(url_for('index'))

@app.route('/login/', methods = ['GET', 'POST'])
def login():
  '''Login form'''   
  error = None
   
  if request.method == 'POST':
      
      usercorrect =  db.session.query(dbmake.Users).filter_by( username = request.form['username'] ).first()

      
      if usercorrect == None: 
        error = "Username not found"
        return render_template(('Login.html') , error = error)

      
      enter = check_password_hash(usercorrect.password,request.form['password'])
      
      if enter == False  :
          error = "Password does not match username"
          return render_template(('Login.html'), error =error)
      
      else:
        session['username'] = request.form['username']
        return redirect(url_for('profile'))

  return render_template('Login.html', error = None)


@app.route('/register/', methods = ['GET' , 'POST'])
def register(): 
  '''Registration form'''
  APP_ROOT = path.dirname(path.abspath(__file__))

  if request.method == 'POST': 
    new_user = dbmake.Users(username = request.form['username'] , password = request.form['password'])
    usercorrect = db.session.query(dbmake.Users).filter_by(username = new_user.username).first()
    
    if usercorrect == None : 
      
      if not new_user.password == request.form['password1'] :
        flash("Sorry! Passwords not matching!")
        return redirect(url_for('index'))

      target = path.join(APP_ROOT , 'static/ImageRepo/')
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

  # if not hasattr(session, 'username'):
  #   return redirect(url_for('login'))
  
  APP_ROOT = path.dirname(path.abspath(__file__))


  if request.method == 'POST' :
    user_details = dbmake.UserData()
    target = path.join(APP_ROOT , 'static/ImageRepo/')
    target = path.join(target, session['username'])
    target = path.join(target,"DisplayPicture/")

    # if not path.exists(target) :
    #   makedirs(target)

    #destination = "/".join([target,"pp"])
    
    pp = request.files['file']
    pp.save(path.join(target,"pp"))

    ImageLocation = "../static/ImageRepo/"+session['username']+"/DisplayPicture/pp"

    user_details.all_details(bio = request.form['bio'] , display_picture = ImageLocation)
    db.session.add(user_details)
    db.session.commit()
    return redirect(url_for('index'))


  return render_template('add_details.html')


@app.route('/user_profile/' , methods = ['GET', 'POST'])
def profile() : 
  ''' User profile '''

  user = db.session.query(dbmake.Users).filter_by(username = session['username']).first()
  
  bio = user.usr.bio

  display_picture = user.usr.image

  return render_template('profile.html', bio = bio, display_picture = display_picture, username = user.username)   


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/add_post/', methods = ['GET' , 'POST'])
def add_post() :
  ''' Adds posts '''

  ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  APP_ROOT = path.dirname(path.abspath(__file__))

  if request.method == 'POST' :

    user = db.session.query(dbmake.Users).filter_by(username = session['username']).first()

    post = dbmake.UserPosts(request.form['caption'], user.id)
    
    target = path.join(APP_ROOT , 'static/ImageRepo/')
    target = path.join(target, session['username'])

    tag1 = request.form['tag1']
    tag2 = request.form['tag2']
    tag3 = request.form['tag3']
    tag4 = request.form['tag4']
    tag5 = request.form['tag5']

    if tag1 :
      tag1 = dbmake.Tags()
    
    pp = request.files['file']

    if pp in allowed_file(pp.filename) : 
      pp.save(path.join(target, str(post.returnp())))

      post.url_image("../static/ImageRepo/" + session['username'] +"/"+ str(post.returnp()))

      db.session.add(post)
      db.session.commit()
      return redirect(url_for('profile'))

    else :
      return " <!doctype html><html><head><title>Upload new File</title></head><body><h1> Improper File type </h1><h2>Upload new File</h2><form action='/add_post/' method=post enctype=multipart/form-data><p><input type=file name=file><input type=submit value=Upload></form></body></html>"  

  return render_template('addpost.html')

@app.route('/searchprof/', methods = ['GET', 'POST'])
def searchprofile() : 
  ''' User profile '''

  if request.method == 'POST':
    userprof = db.session.query(dbmake.Users).filter_by(username = request.form['Search']).first()
  
    bio = userprof.usr.bio

    test=[]

    display_picture = userprof.usr.image

    posts = db.session.query(dbmake.UserPosts).filter_by(user_id = userprof.id).all()

    thisuser = db.session.query(dbmake.Users).filter_by(username = session['username']).first()

    followflag = []

    followflag = db.session.query(dbmake.Follows).filter_by(follower_id = thisuser.id, following_id = userprof.id ).first()

    return render_template('searchprofile.html', username=userprof.username, bio = bio, display_picture = display_picture, posts = posts, thisuserid=thisuser.id, userid=userprof.id, followflag = followflag)

  return render_template('searchperson.html')

@app.route('/feed/' , methods = ['GET' , 'POST'])
def feed() :
  ''' User's feed '''

  if request.method == 'POST':
    
    post_id = request.form['post_id']
    like_id = request.form['like_id']
    unlike = request.form['unlike']

    posttobeupdated = db.session.query(dbmake.UserPosts).filter_by(id = post_id).first()
    print(posttobeupdated.retnolikes())
    userupdating = db.session.query(dbmake.Users).filter_by(username = session['username']).first()
    print(userupdating.id)
    print(unlike)

    if unlike == "true" : 
      print("Postneeds to be unlikesd")
      posttobeupdated.unlike_post()
      db.session.query(dbmake.Likes).filter_by(post_id = posttobeupdated.id , user_id = userupdating.id).delete()
      likeid=""
      db.session.commit()

    else : 
      print("Post needs to be liked")
      posttobeupdated.like_post(userupdating.id)
      likep = db.session.query(dbmake.Likes).filter_by(user_id = userupdating.id , post_id = posttobeupdated.id).first()
      likeid = likep.id
      db.session.commit()

    like_count = posttobeupdated.retnolikes()
    print(like_count)

    return jsonify({'count' : like_count, 'like_id' : likeid })
    

  f_id = db.session.query(dbmake.Users).filter_by(username = session['username']).first()

  follows = db.session.query(dbmake.Follows).filter_by(follower_id = f_id.id).all()
  posts=[]  

  for follow in follows:
    picturelist = db.session.query(dbmake.UserPosts).filter_by(user_id = follow.following_id).all()
    for singlepost in picturelist:
      posts.append(singlepost)

  posts.sort(key = lambda x : x.id , reverse = True)
  
  return render_template('userfeed.html', posts = posts)



@app.route('/comments/', methods = ['GET', 'POST'])
def comment() : 

  if request.method == 'POST' : 

    post_id = request.form['post_id']
    comment_id = request.form['comment_id']   

    print(post_id , " " , comment_id , " " , request.form['comment'])

    posttobeupdated = db.session.query(dbmake.UserPosts).filter_by(id = post_id).first() 
    userupdating = db.session.query(dbmake.Users).filter_by(username = session['username']).first()

    posttobeupdated.comment_post(userupdating.id, request.form['comment'])
    
    comment_id = db.session.query(dbmake.Comments).filter_by(user_id = userupdating.id , post_id = posttobeupdated.id).first()

    db.session.commit()

    return jsonify({'count' : like_count, 'comment_id' : comment_id.id })



@app.route('/follow/<id>', methods = ['GET', 'POST'])
def followperson(id):
  thisuser = db.session.query(dbmake.Users).filter_by(username = session['username']).first()
  follow=dbmake.Follows(thisuser.id, id)
  db.session.add(follow)
  db.session.commit()
  return render_template('searchperson.html')


@app.route('/unfollow/<id>', methods = ['GET', 'POST'])
def unfollowperson(id):
  thisuser = db.session.query(dbmake.Users).filter_by(username = session['username']).first()
  db.session.query(dbmake.Follows).filter_by(follower_id = thisuser.id, following_id = id ).delete()
  db.session.commit()
  return render_template('searchperson.html')

if __name__ == "__main__" :
   app.run(debug = True)