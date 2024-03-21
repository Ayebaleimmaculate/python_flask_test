from authors_app import db

from datetime import datetime


class Company(db.Model):
    __tablename__='companies'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),unique=True)
    orign = db.Column(db.String(100),nullable=False)
    description = db.Column(db.Text(),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    user = db.relationship('user',backref='companies')
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())
# creating a constructor class
def __init__(self,name,orign,description,user_id):
    super(Company,self).__init__ ()
    self.name = name
    self.orign = orign
    self.description = description
    self.user_id= user_id

def __repr__(self):
    return f"<company(name='{self.name}',origin=' {self.orign}')"


