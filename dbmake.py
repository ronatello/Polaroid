from sqlalchemy import Column, ForeignKey, Integer, String
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
	one_thing = relationship(Users, backref=backref('other_thing', uselist=False))
	#user_id = Column(Integer(), ForeignKey('userauth.id'))
	bio = Column(String(250))
	image = Column(String(250))

	# user = relationship(Users)

	def __init__(self) :
		self.bio = None 
		self.posts = None

	def bio_update() :
		pass

	def display_picture() :
		pass

	# more individual update things 

	def all_details(self, bio, display_picture) :
		self.bio = bio 
		self.dimage = display_picture

	def get_id(self) : 
		return self.id ; 

Base.metadata.create_all(engine)

query=session.query(Users).outerjoin(UserData)

for P in query:
	print (P.id,P.username,P.other_thing.bio, P.other_thing.display_picture)
	
	
