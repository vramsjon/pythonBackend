from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello coder"

@app.route("/data")
def get_data():
    data = {
        "name": "Vramsjon Piter Hutagalung",
        "age": 23,
        "city": "Bandung"
    }
    return jsonify(data)

@app.route("/info")
def get_info():
    info = {
        "version" : "1.0",
        "status" : "API is running"
    }
    return jsonify(info)
if __name__ == "__main__":
    app.run(debug=True)