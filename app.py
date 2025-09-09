import json, random, os
from flask import Flask, render_template, request, redirect, url_for

BASE = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE, "data", "destinations.json")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
    q = request.args.get("q","").strip().lower()
    category = request.args.get("category","")
    data = load_data()
    results = data["destinations"]
    if q:
        results = [d for d in results if q in d["name"].lower() or q in d.get("description","").lower() or any(q in t.lower() for t in d.get("tags",[]))]
    if category:
        results = [d for d in results if d.get("category","")==category]
    # sort by rating desc
    results = sorted(results, key=lambda x: x.get("rating",0), reverse=True)
    categories = sorted(set(d.get("category","") for d in data["destinations"]))
    return render_template("index.html", results=results, categories=categories, q=q, category=category)

@app.route("/destination/<slug>")
def destination(slug):
    data = load_data()
    dest = next((d for d in data["destinations"] if d["slug"]==slug), None)
    if not dest:
        return redirect(url_for("index"))
    return render_template("destination.html", d=dest)

@app.route("/random")
def random_dest():
    data = load_data()
    dest = random.choice(data["destinations"])
    return redirect(url_for("destination", slug=dest["slug"]))

@app.route("/quiz")
def quiz():
    # simple quiz: pick 4 random destinations, ask which state matches first one's festival
    data = load_data()
    choices = random.sample(data["destinations"], k=min(4, len(data["destinations"])) )
    question = {
        "prompt": f"Which state hosts the festival: {choices[0].get('highlight','a local special event')}?",
        "answer": choices[0]["state"],
        "choices": [c["state"] for c in choices],
        "explain": choices[0].get("fun_fact","")
    }
    return render_template("quiz.html", q=question)
@app.route("/ganjam")
def ganjam():
    return render_template("ganjam.html")

@app.route("/ganjam/festivals")
def ganjam_festivals():
    return render_template("ganjam_festivals.html")

@app.route("/ganjam/tribes")
def ganjam_tribes():
    return render_template("ganjam_tribes.html")

@app.route("/ganjam/art")
def ganjam_art():
    return render_template("ganjam_art.html")

@app.route("/ganjam/hidden")
def ganjam_hidden():
    return render_template("ganjam_hidden.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
