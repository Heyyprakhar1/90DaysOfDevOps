from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    # Serve index.html from root
    return render_template("index.html")

@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
