# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class App(db.Model):
#     name = db.Column(db.String(200), primary_key=True)
#     link = db.Column(db.String(500), unique=True, nullable=False)
#     logo = db.Column(db.String(500))
#     description = db.Column(db.Text)

#     def to_dict(self):
#         return {
#             "name": self.name,
#             "link": self.link,
#             "logo": self.logo,
#             "description": self.description,
#         }
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AndroidApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    package_name = db.Column(db.String(100), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    downloads = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    developer = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(200), nullable=True)
