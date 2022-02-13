from flask import Flask, request

from lib.conf import conf
from lib.hat import Hat

app = Flask(__name__)
app.hat = Hat()
app.hat.off()


@app.route("/light", methods=["POST"])
def light():
    """Light a light."""
    colour = [255, 255, 255]
    data = request.get_json()
    if "colour" in data:
        colour = data["colour"]
    app.hat.off()
    app.hat.light_one(data["index"], colour)

    return {"status": "OK"}


@app.route("/light-all", methods=["POST"])
def light_all():
    """Light all the lights."""
    app.hat.light_all([255, 255, 255])

    return {"status": "OK"}


if __name__ == "__main__":  # nocov
    app.run(host="0.0.0.0", port=conf["webserver-port"])
