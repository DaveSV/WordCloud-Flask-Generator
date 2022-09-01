import numpy as np
from flask import Flask, request, jsonify, render_template, url_for, send_file
from PIL import Image
import wikipedia
from wordcloud import WordCloud, STOPWORDS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wcg', methods=["POST","GET"])
def wcg():
    contador = 0
    if request.method == "POST":
        words = request.form["words"]
        count = request.form["count"]
        height = request.form["height"]
        width = request.form["width"]
        minfontsize = request.form["minfontsize"]
        maxfontsize = request.form["maxfontsize"]
    
        count = int(count)
        width = int(width)
        height = int(height)
        minfontsize = int(minfontsize)
        maxfontsize = int(maxfontsize)
        
        title = wikipedia.search(words)[0]
        page = wikipedia.page(title)

        contador = 1
     
        # print(page.content)
        background = np.array(Image.open("cloud.png"))
        stopwords = set(STOPWORDS)

        wc = WordCloud(background_color="white",
                    max_words=count,
                    width = width,
                    min_font_size = minfontsize,
                    max_font_size = maxfontsize,
                    height = height,
                    mask = background,
                    stopwords = stopwords)
        
        wc.generate(page.content)
        wc.to_file("static/img/wordcloud.png")

        # filename = Image.open("wordcloud.png")
        # filename.show()
        
        return render_template('wcg.html', contador=contador)
    else:
        return render_template('wcg.html', contador=contador)

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/download')
def download():
    path = 'static/img/wordcloud.png'
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
