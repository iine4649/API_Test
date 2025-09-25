from flask import Flask, jsonify
import random


import json
import os

jokes_file_path = os.path.join(os.path.dirname(__file__), "jokes.json")
with open(jokes_file_path, "r", encoding="utf-8") as f:
    jokes = json.load(f)

app = Flask(__name__)



@app.route("/")
def home():
    home_file_path = os.path.join(os.path.dirname(__file__), "home.html")
    with open(home_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return html_content

@app.route("/api/joke")
def get_joke():
    return jsonify(random.choice(jokes))

###############################################################################
# Now you need to add a route parameter! Think about how we can do this using #
# our python logic after I show you how to insert a route parameter.          #
###############################################################################

if __name__ == "__main__":
    app.run()
