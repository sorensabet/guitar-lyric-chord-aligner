import os
from helpers import convert_lyrics
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = ''
    converted_lyrics = ''
    image_paths = []
    
    if request.method == 'POST':
        user_input = request.form['user_input']
        converted_lyrics, image_paths = convert_lyrics(user_input)

    return render_template('index.html', 
                           input=user_input, 
                           converted_lyrics=converted_lyrics,
                           image_paths=image_paths)

if __name__ == '__main__':
    app.run()
