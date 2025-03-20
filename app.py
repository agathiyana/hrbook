from flask import Flask, jsonify, request, redirect, url_for


app = Flask(__name__)

@app.route('/ctracker')
def ctracker():
    return open('templates/ctracker.html').read()  # Serve the main page



if __name__ == '__main__':
    app.run(debug=True)
