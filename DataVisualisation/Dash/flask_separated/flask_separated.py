import os
import sys
from flask import Flask
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)
from dash_application import dash_example

app = Flask(__name__)

dash = dash_example.dash_application()
dash.init_app(app=app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
    
if __name__ == '__main__':
    app.run(debug=True)