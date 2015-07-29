from flask import Flask
app = Flask(__name__)

@app.route("/")
def ping():
    return "python server received 'ping' request!"

if __name__ == "__main__":
    app.run(debug=True)

