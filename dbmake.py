from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship , sessionmaker, backref
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash

Base = declarative_base()
engine = create_engine('sqlite:///elephant.db')

Base.metadata.bind = engine

eleSession = sessionmaker(bind = engine)
session = eleSession() 

class Users(Base) : 
	'''Table containing user authentication details '''
	__tablename__ = 'userauth'

	id = Column(Integer(), primary_key = True, autoincrement = True ) 
	username = Column(String(50), unique = True, nullable = False)
	password = Column(String(100), nullable = False)

	def __init__ (self, username, password) : 
		self.username = username 
		self.password = generate_password_hash(password)



class UserData(Base) : 
	''' Contains bio of users, interests, history(likes, comments ) , links to images  ''' 
	__tablename__ = 'userdata'

	id = Column(Integer() ,ForeignKey(Users.id), primary_key = True, autoincrement = True)
	dat = relationship(Users, backref=backref('usr', uselist=False))
	#user_id = Column(Integer(), ForeignKey('userauth.id'))
	bio = Column(String(250))
	image = Column(String(250))

	# user = relationship(Users)

	def __init__(self) :
		self.bio = None 
		self.posts = None
		self.display_picture = None

	def bio_update(self, bio) :
		self.bio= bio

	def display_picture(self, display_picture ) :
		self.image = display_picture

	# more individual update things 

	def all_details(self, bio, display_picture) :
		self.bio = bio 
		self.image = display_picture

	def get_id(self) : 
		return self.id ; 

class UserPosts(Base) : 
	'''Contains all information pertaining to a post and ties it with the user that has posted it.
		Likes, users that have liked, comments and respective users, tags nrn, share, pinned posts(?), tagging people, crop'''
	
	__tablename__ = 'postcontent'

	id = Column(Integer() , primary_key = True , autoincrement = True) 
	p=0 
	user_id = Column(Integer(), ForeignKey(Users.id))
	post = relationship(Users)
	caption = Column(Text())
	image = Column(String(150))
	llikes = Column(Integer())
	ccomments = Column(Integer())

	def get_id(self) : 
		return self.user_id

	def get_post_id(self) : 
		return self.id

	def __init__ ( self, caption, users) :
		self.caption = caption 
		self.user_id = users
		self.llikes = 0
		self.comment = 0

	def returnp(self) :
		return self.__class__.p

	def url_image(self, image):
		self.image = image

	def like_post(self, userid):
		post_like = Likes(userid, self.id) # we get user id by using session['username']
		self.llikes += 1
		session.add(post_like)
		session.commit()

	def comment_post(self, userid, comment) : 
		post_comment = Comments(userid, self.id , comment)
		self.comment += 1
		session.add(post_comment)
		session.commit()


class Likes(Base):


	__tablename__ = 'postlikes'

	id = Column(Integer(), primary_key = True, autoincrement = True)
	user_id = Column(Integer(), ForeignKey(Users.id))
	post_id = Column(Integer(), ForeignKey(UserPosts.id))
	likepost = relationship(UserPosts, backref = backref('lpost', uselist = False))
	likeuser = relationship(Users, backref = backref('luser', uselist = False))

	def __init__(self, userid, postid):
		self.user_id = userid
		self.post_id = postid

class Comments(Base):

	__tablename__ = 'postcomments'

	id = Column(Integer(), primary_key = True, autoincrement = True)
	user_id = Column(Integer(), ForeignKey(Users.id))
	post_id = Column(Integer(), ForeignKey(UserPosts.id))
	comment = Column(Text())
	commentpost = relationship(UserPosts, backref = backref('cpost', uselist = False))
	commentuser = relationship(Users, backref = backref('cuser', uselist = False))

	def __init__(self, userid, postid, comment):
		self.user_id = userid
		self.post_id = postid
		self.comment = comment






Base.metadata.create_all(engine)

# query=session.query(Users).outerjoin(UserData)

# for P in query:
# 	print (P.id,P.username,P.other_thing.bio, P.other_thing.display_picture)
	
	
