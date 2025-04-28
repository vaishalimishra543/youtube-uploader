from flask import Flask, render_template, request
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', formats=None)

@app.route('/fetch_formats', methods=['POST'])
def fetch_formats():
    youtube_url = request.form['youtube_url']
    cookies_file = request.form['cookies_file']  # Get the cookies file path from the form

    ydl_opts = {
        'quiet': True,
        'cookies': cookies_file  # Pass the cookies path to yt-dlp
    }
    
    try:
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
        return render_template('index.html', formats=formats, youtube_url=youtube_url, cookies_file=cookies_file)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/download_selected', methods=['POST'])
def download_selected():
    youtube_url = request.form['youtube_url']
    format_id = request.form['format_id']
    cookies_file = request.form['cookies_file']  # Get the cookies file path from the form

    ydl_opts = {
        'format': format_id,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookies': cookies_file  # Pass the cookies path to yt-dlp
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            file_title = ydl.prepare_filename(info)
        
        return f"✅ Downloaded {os.path.basename(file_title)} successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
