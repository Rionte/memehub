from flask import Flask
from flask import render_template, request, flash
from werkzeug.utils import secure_filename
import sqlite3

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conn = sqlite3.connect("memes.db")
cur = conn.cursor()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello():
    ctx = {}
    return render_template("base.html", ctx=ctx)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("HI")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    #app.secret_key = 'memehubrionte'
    #app.config['SESSION_TYPE'] = 'filesystem'
    #sess.init_app(app)
    app.run(host='127.0.0.1')