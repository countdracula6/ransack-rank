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
        keyword = request.form.get("keyword") or None

        if url:
            result = analyze_seo(url, target_keyword=keyword)

    return render_template("seo.html", result=result)

@app.route("/compare", methods=["GET", "POST"])
def compare():
    result1 = None
    result2 = None

    if request.method == "POST":
        url1 = request.form.get("url1")
        url2 = request.form.get("url2")

        if url1 and url2:
            result1 = analyze_seo(url1)
            result2 = analyze_seo(url2)

    return render_template("compare.html", result1=result1, result2=result2)

# Optional: Local dev run (Render uses gunicorn instead)
if __name__ == "__main__":
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)))