from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    username = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    blog = db.relationship('Blog',backref = 'user',lazy = "dynamic")


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(pasword)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)            


    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text(),nullable=False)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship('Comment', backref='blog', lazy='dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blog(cls,id):
        blog = Blog.query.filter_by(id=id).first()
        return blog





class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'        



