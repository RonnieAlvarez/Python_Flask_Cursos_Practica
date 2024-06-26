from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# -------   tuve que usar flask shell para aplicar el  db.create_all() y crear las tablas con sus relaciones
class User(db.Model, UserMixin):
    __tablename__='user_login'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    
    courses = db.relationship('Courses', backref='user_login', lazy=True)

    def set_password(self,password):
        # conviete en hash el password
        self.password=generate_password_hash(password)
        
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

