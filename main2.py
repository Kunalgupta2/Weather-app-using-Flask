from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///name.db"
db=SQLAlchemy(app)
class Name(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    city=db.Column(db.String(50), nullable=False)

@app.route("/", methods=["GET", "POST"])
def geolocation():
    if request.method=="POST":
        city=request.form["city"]
        newcity=Name(city=city)
        db.session.add(newcity)
        db.session.commit()
    else:
        city="delhi"

    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=5589e060a33a1eed6ea407362fb289bb"
    response=requests.get(url)
    response=response.json()
    weather={
        "city":city,
        "temperature":response["main"]["temp"],
        "description":response["weather"][0]["description"],
        "icon":response["weather"][0]["icon"]
    }
    return render_template("index.html", weather=weather)

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)




