from flask import Flask, render_template, request
from scraper.seo import analyze_seo

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/seo", methods=["GET", "POST"])
def seo():
    result = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            result = analyze_seo(url)
    return render_template("seo.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
