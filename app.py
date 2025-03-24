<<<<<<< HEAD
from flask import Flask, jsonify, request, redirect, url_for
import email_scheduler
=======
from flask import Flask, jsonify, request, redirect, url_for,render_template

>>>>>>> 7b7415971e574f29836db253797191501629d642

app = Flask(__name__)

@app.route('/ctracker')
def ctracker():
    req_list = ['QA-Automation-Selenium-API-Jan', 'QA-Automation-Selenium-ETL-March', 'QA-Automation-Selenium-API-Mar', 'QA-Automation-Selenium-API-Feb']  
    # return open('templates/ctracker.html').read()  # Serve the main page
    return render_template('ctracker.html', req_list=req_list)

<<<<<<< HEAD
=======

@app.route('/requirements')
def manage_requirements():
    req_list = ['QA-Automation-Selenium-API-Jan', 'QA-Automation-Selenium-ETL-March', 'QA-Automation-Selenium-API-Mar', 'QA-Automation-Selenium-API-Feb']  
    return render_template('requirements.html', req_list=req_list)


>>>>>>> 7b7415971e574f29836db253797191501629d642
if __name__ == '__main__':
    finalstatus = "completed"
    email_scheduler(finalstatus)
    app.run(debug=True)
