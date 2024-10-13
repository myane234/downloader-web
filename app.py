from flask import Flask, request, render_template, redirect, url_for
import subprocess
import os

app = Flask(__name__)

# Lokasi tempat file yang diunduh dan playlist disimpan
DOWNLOAD_FOLDER = 'static/downloaded_files'
PLAYLIST_FILE = 'playlist.txt'

# Membuat folder download dan file playlist jika belum ada
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

if not os.path.exists(PLAYLIST_FILE):
    open(PLAYLIST_FILE, 'w', encoding='utf-8').close()  # Menggunakan encoding UTF-8 saat membuat file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    file_format = request.form['format']

    try:
        if file_format == 'mp3':
            subprocess.run(['yt-dlp', '-x', '--audio-format', 'mp3', '-o', f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s', url], check=True)
            return redirect(url_for('playlist'))  # Redirect ke halaman playlist setelah selesai download
        elif file_format == 'mp4':
            subprocess.run(['yt-dlp', '-f', 'bestvideo+bestaudio', '-o', f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s', url], check=True)
            return redirect(url_for('playlist'))  # Redirect ke halaman playlist setelah selesai download
    except subprocess.CalledProcessError:
        return "Gagal mengunduh file."

@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    # Baca file audio yang sudah diunduh
    downloaded_files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith('.mp3')]

    # Jika ada request POST untuk menambah ke playlist
    if request.method == 'POST':
        selected_file = request.form['file']
        with open(PLAYLIST_FILE, 'a', encoding='utf-8') as file:  # Menulis dengan encoding UTF-8
            file.write(selected_file + '\n')
        return redirect(url_for('playlist'))

    # Baca playlist dari file
    with open(PLAYLIST_FILE, 'r', encoding='utf-8') as file:  # Membaca dengan encoding UTF-8
        playlist = [line.strip() for line in file.readlines()]

    return render_template('playlist.html', downloaded_files=downloaded_files, playlist=playlist)

if __name__ == '__main__':
    app.run(debug=True)
