from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/data')
def get_data():
    data = {
        "cells": [587, 3336, 411, 175, 73, 808, 29, 275, 44404, 4146, 101, 987, 797, 41, 46, 2775, 347, 131, 212, 4241, 711, 233, 378, 4230, 800, 76, 1131]
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
