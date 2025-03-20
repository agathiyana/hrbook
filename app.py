from flask import Flask, jsonify, request, redirect, url_for,render_template


app = Flask(__name__)

@app.route('/ctracker')
def ctracker():
    req_list = ['QA-Automation-Selenium-API-Jan', 'QA-Automation-Selenium-ETL-March', 'QA-Automation-Selenium-API-Mar', 'QA-Automation-Selenium-API-Feb']  
    # return open('templates/ctracker.html').read()  # Serve the main page
    return render_template('ctracker.html', req_list=req_list)


@app.route('/requirements')
def manage_requirements():
    req_list = ['QA-Automation-Selenium-API-Jan', 'QA-Automation-Selenium-ETL-March', 'QA-Automation-Selenium-API-Mar', 'QA-Automation-Selenium-API-Feb']  
    return render_template('requirements.html', req_list=req_list)


if __name__ == '__main__':
    app.run(debug=True)
