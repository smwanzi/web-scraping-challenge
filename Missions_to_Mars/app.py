from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo
import scrape_mars

#create an instance of Flask App
app = Flask(__name__)

#Use flask_pymongo to set up mongo connections
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


#set the route to render index.html template using data from Mongo
@app.route("/")
def index():
    try:
        mars = mongo.db.mars.find_one()
        return render_template('index.html', mars=mars)
    except:
        redirect("/scrape", code=302)       
#scrape route
@app.route("/scrape")
def scrape():
    mongo.db.mars.drop()
    mars_data = scrape_mars.scrape()
    mongo.db.mars.insert_one(mars_data)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
