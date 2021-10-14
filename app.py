
#################################################################
# MODULE 10.5.1 - Use Flask to Create a Web App
#################################################################

# Use Flask to render a template, redirect to another url, 
# and create a URL.
from flask import Flask, render_template, redirect, url_for
# Use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo
# Use the scraping code, we will convert from Jupyter notebook 
# to Python.
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
## Tell Python that our app will connect to Mongo using a URI (similar to a URL)
## In this case, the URI we are using is "mongodb://localhost:27017/mars_app"
## which is telling the app to connect to Mongo through our localhost server
## using port 27017, using a database named "mars_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# 
mongo = PyMongo(app)

#############################
# Set Up App Routes
#############################

# Step 1: define the route for the HTML page.

@app.route("/")
def index():
   # Use PyMongo to find the "mars" collection in our database and
   # assign it the path it finds to a variable named 'mars' for
   # later use.
   mars = mongo.db.mars.find_one()
   # Tell Flask to return an HTML template using an index.html file.
   # mars-mars tells Python to use the "mars" collection in MongoDB.
   return render_template("index.html", mars=mars)

# Step 2: set up our scraping route. This route will be the "button" 
# of the web application, the one that will scrape updated data when 
# we tell it to from the homepage of our web app. It'll be tied to a
# button that will run the code when it's clicked.

@app.route("/scrape")
def scrape():
   # Assign a new variable that points to our Mongo database
   mars = mongo.db.mars
   # Create a new variable to hold the newly scraped data.
   # scraping refers to the scraping.py code file previously created 
   # in MODULE 3.4, and scrape_all refers to the function contained
   # in the scraping.py code file.
   mars_data = scraping.scrape_all()
   # Update the database using the update method, where the {} is the
   # query parameter, mars_data is the data, and upsert=True is one
   # of the method's options. In this case, the {} is indicating we
   # want to create and empty JSON object. The upsert=True is telling
   # Mongo to create a new document if one doesn't already exist.
   # the data
   mars.update({}, mars_data, upsert=True)
   # Finally, a redirect will return to the home page so that we can
   # see the updated content.
   return redirect('/', code=302)

# Tell Flask to run the app.
if __name__ == "__main__":
   app.run()