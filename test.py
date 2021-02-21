from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Restaurant(db.Model):
    __tablename__ = "restaurants"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    kitchen = db.Column(db.String)


db.create_all()


db.session.add(Restaurant(name="Pelmeni", kitchen="Russian"))
db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
