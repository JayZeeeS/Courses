from flask import Flask, render_template, request

app = Flask(__name__)

COLORS = ["red", "blue"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        print("Form submitted!")
        color = request.form.get("color")
        if color not in COLORS:
            return render_template("failure.html", color=color.capitalize())
        return render_template("color.html", color=color)