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
    rates = db.relationship("Rate")

    def get_rating(self):
        sum = 0
        for restaurant in self.rates:
            sum += restaurant.rating
        return "{} {}".format(restaurant.restaurant.name, sum / len(self.rates))


class User(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rates = db.relationship("Rate")


class Rate(db.Model):
    __tablename__ = "rates"
    uid = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    user = db.relationship("User")
    restaurant = db.relationship("Restaurant")
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.uid"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.uid"))


db.create_all()

lstRes = []
for _ in range(3):
    restaurant = input().split(",")
    lstRes.append(Restaurant(uid=restaurant[0], name=restaurant[1], kitchen=restaurant[2]))
db.session.add_all(lstRes)
db.session.commit()

lstUs = []
for _ in range(3):
    user = input().split(",")
    lstUs.append(User(uid=user[0], name=user[1]))
db.session.add_all(lstUs)
db.session.commit()

lstRat = []
for _ in range(9):
    data = input().split(",")
    restaurant = Restaurant.query.get(data[0])
    user = User.query.get(data[1])
    lstRat.append(Rate(rating=data[2], user=user, restaurant=restaurant))
db.session.add_all(lstRat)
db.session.commit()

restaurants = Restaurant.query.all()
users = User.query.all()
ratings = Rate.query.all()
for res in restaurants:
    print(res.get_rating())

if __name__ == "__main__":
    app.run(debug=False)
