from flask import Flask, render_template, request
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', formats=None)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
