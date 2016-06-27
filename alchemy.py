from sqlalchemy import Column,String,Integer,create_engine,Sequence,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
import os
import random
from faker import Faker

fake = Faker()

Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	id = Column(Integer,primary_key = True)
	name = Column(String())
	password = Column(String())
	nation_id = Column(Integer,ForeignKey('nations.id'))
	def __repr__(self):
		return 'user:id=%5s,name=%25s,password=%20s,nation=%10s' %(self.id,self.name,self.password,self.nation_id)

class Nation(Base):
	__tablename__ = 'nations'
	id = Column(Integer,primary_key = True)
	name = Column(String())
	postcode = Column(String())
	users = relationship("User")
	def __repr__(self):
		return 'nation:id %10s,name%25s,postcode %20s' %(self.id,self.name,self.postcode)


db_name = 'data.sqlite'
db_url = 'sqlite:///'+ os.path.join(os.path.dirname(__file__),db_name)
# print db_url
engine = create_engine(db_url,echo =False)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def run_once():
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)
	users = [User(name =fake.name(),password = fake.password(),nation_id = random.randrange(1,20)) for i in range(999)]
	session.add_all(users)
	nations = [Nation(name=fake.country(),postcode=fake.postcode()) for i in range(30)]
	session.add_all(nations)
	session.commit()

def show_all_tables():
	print "-"*100
	for item in session.query(User):
		print item

	print "-"*100
	for item in session.query(Nation):
		print item

# run_once()
def test_query():
	for user in session.query(User).join(Nation).filter(Nation.name=="Korea"):
		print user
	# for item in session.query(Nation).join(User).filter():
	# 	# print item.users,"|"*50
	# 	print "="*100
	# 	for user in item.users:
	# 		print user
if __name__ == "__main__":
	# show_all_tables()
	test_query()
	session.close()
