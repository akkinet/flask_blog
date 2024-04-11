from flask import Flask
import sqlite3

DATABASE = "blog.db"
app = Flask(__name__)

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

if __name__ == "__main__":
    app.run(debug=True)