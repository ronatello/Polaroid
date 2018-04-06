from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship , sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///elephant.db')

Base.metadata.bind = engine

eleSession = sessionmaker(bind = engine)
session = eleSession() 

class Users(Base) : 
	'''Table containing user authentication details '''
	__tablename__ = 'userauth'

	id = Column(Integer(), primary_key = True ) 
	username = Column(String(50), unique = True, nullable = False)
	password = Column(String(100), nullable = False)

	def __init__ (self, username, password) : 
		self.username = username 
		self.password = password

class UserData(Base) : 
	''' Contains bio of users, interests, history(likes, comments ) , links to images  ''' 
	__tablename__ = 'userdata'

	id = Column(Integer() , primary_key = True)
	user_id = Column(Integer, ForeignKey('user.id'))
	bio = Column(String(250))
	image = Column(String(150))

	user = relationship(Users)



	def __init__(self) :
		self.bio = None 
		self.posts = None
		self.display_picture = None

	def bio_update() :
		pass

	def display_picture() :
		pass

	# more individual update things 

	def all-details(self, bio, display_picture) :
		self.bio = bio 
		self.display_picture = display_picture



Base.metadata.create_all(engine)

# Person = session.query(Users).first()

# print (Person.username, " " , Person.password)