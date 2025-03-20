from flask import Flask, jsonify, request, redirect, url_for
import email_scheduler

app = Flask(__name__)

@app.route('/ctracker')
def ctracker():
    return open('templates/ctracker.html').read()  # Serve the main page

if __name__ == '__main__':
    finalstatus = "completed"
    email_scheduler(finalstatus)
    app.run(debug=True)
