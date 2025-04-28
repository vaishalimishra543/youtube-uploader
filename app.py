from flask import Flask, render_template, request
import yt_dlp
import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

app = Flask(__name__)

# Setup Google Drive authentication
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', formats=None)

@app.route('/fetch_formats', methods=['POST'])
def fetch_formats():
    youtube_url = request.form['youtube_url']
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        formats = [
            {
                'format_id': f['format_id'],
                'format_note': f.get('format_note', ''),
                'ext': f.get('ext', ''),
                'filesize': f.get('filesize')
            }
            for f in info['formats'] if f.get('filesize')
        ]
    return render_template('index.html', formats=formats, youtube_url=youtube_url)

@app.route('/download_selected', methods=['POST'])
def download_selected():
    youtube_url = request.form['youtube_url']
    format_id = request.form['format_id']
    ydl_opts = {'format': format_id, 'outtmpl': 'downloads/%(title)s.%(ext)s'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        file_title = ydl.prepare_filename(info)

    # Upload to Google Drive
    file = drive.CreateFile({'title': os.path.basename(file_title)})
    file.SetContentFile(file_title)
    file.Upload()

    return f"✅ Uploaded {os.path.basename(file_title)} to your Google Drive!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
