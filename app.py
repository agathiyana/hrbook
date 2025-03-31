import os
import secrets
import sqlite3
from flask import  Flask, flash, jsonify, render_template, request, redirect, session, url_for
import matplotlib.pyplot as plt
import io
import base64
from email_scheduler import email_scheduler
app = Flask(__name__)
app.secret_key = os.urandom(24)
global color
DATABASE = 'requirementlist.db'

def get_db():
    """Returns a connection to the SQLite database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows access to columns by name
    return conn

def init_db():
    """Initialize the database with required table"""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS requirementdetail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                requirementname String NOT NULL,
                clientname String NOT NULL,
                clientmanager String NOT NULL,
	            departmentname String NOT NULL,
	            accountmanager String NOT NULL,
	            jobdescription String NOT NULL,
	            workexperience String NOT NULL,
	            openposition String NOT NULL,
	            timing String NULL,
	            locationname String NULL,
	            workmode String NOT NULL,
	            recruiter String NULL,
	            budget String NULL,
	            comment String NULL,
	            startdate String NOT NULL,
	            enddate String  NULL,
	            display String NOT NULL,
	            status String NOT NULL
            )
        ''')
        conn.commit()

@app.route('/ctracker')
def ctracker():
    req_list = ['QA-Automation-Selenium-API-Jan', 'QA-Automation-Selenium-ETL-March', 'QA-Automation-Selenium-API-Mar', 'QA-Automation-Selenium-API-Feb']  
    # return open('templates/ctracker.html').read()  # Serve the main page
    return render_template('ctracker.html', req_list=req_list)

@app.route('/graph')
def graph():
     with get_db() as conn:
            curs = conn.cursor()
            curs.execute('SELECT * FROM requirementdetail')
            requirementdetail = curs.fetchall()

            labels = [row[2] for row in requirementdetail]
            counts = [row[8] for row in requirementdetail]

    # Create a figure and axis
     fig, ax = plt.subplots()
     fig, ax = plt.subplots()
     ax.bar(labels, counts, color='skyblue')
     ax.set_xlabel('clientname')
     ax.set_ylabel('openposition')
     ax.set_title('Client Opening Report')
    # Data for the bar chart

    # Save the figure to a BytesIO object in PNG format
     img = io.BytesIO()
     fig.savefig(img, format='png')
     img.seek(0)  # Rewind the file pointer to the beginning

    # Encode the image as a base64 string to display in the browser
     img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    # Return the image as a response
     return render_template('graph.html', graph=img_base64)
    #req_list = ['QA-Automation-Selenium-API-Jan', 'QA-Automation-Selenium-ETL-March', 'QA-Automation-Selenium-API-Mar', 'QA-Automation-Selenium-API-Feb']  
    # return open('templates/ctracker.html').read()  # Serve the main page
    #req_list=req_list


@app.route('/reg')
def test():
    return render_template('reg.html')

@app.route('/managerequirement',methods=['GET', 'POST'])
def managerequirement():
    
    if request.method == 'POST':
    # Retrieve form data
        requirementname = request.form['requirementname']
        clientname = request.form['clientname']
        clientmanager = request.form['clientmanager']
        departmentname = request.form['departmentname']
        accountmanager = request.form['accountmanager']
        jobdescription = request.form['jobdescription']
        workexperience = request.form['workexperience']
        openposition = request.form['openposition']
        timing = request.form['timing']
        locationname = request.form['locationname']
        workmode = request.form['workmode']
        recruiter = request.form['recruiter']
        budget = request.form['budget']
        comment = request.form['comment']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        display = request.form['display']
        status = request.form['status']
        app.logger.warning("A warning message."+requirementname)  
        recorddata = requirementname
    # Insert into database
        with get_db() as conn:
            curs = conn.cursor()
            curs.execute('''
            INSERT INTO requirementdetail (requirementname, clientname, clientmanager, departmentname, accountmanager,
                                    jobdescription, workexperience, openposition,timing,locationname,workmode,recruiter,budget,comment, startdate, enddate, display, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?)
        ''', (requirementname, clientname, clientmanager, departmentname, accountmanager, jobdescription,
              workexperience, openposition,timing,locationname,workmode,recruiter,budget,comment, startdate, enddate, display, status))
            conn.commit()
            if curs.rowcount > 0:
                alert_message = f"Record added successfully! Requirement Name: {recorddata}"
            else:
                alert_message = 'Record not added. Requirement Name: {recorddata}'
            return redirect(url_for('managerequirement',alert=alert_message))
    else:
        with get_db() as conn:
            curs = conn.cursor()
            curs.execute('SELECT * FROM requirementdetail')
            requirements = curs.fetchall()
            return render_template('requirements.html',requirements=requirements)

# Route to delete a record
@app.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    global recorddata
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT requirementname from requirementdetail WHERE id = ?", (record_id,))
    recorddata = cur.fetchone()
    # DELETE query to remove the record with the given ID
    cur.execute("DELETE FROM requirementdetail WHERE id = ?", (record_id,))
    conn.commit()  # Commit the changes to the database
    if cur.rowcount > 0:
            alert_message = f"Record deleted successfully! Requirement Name: {recorddata['requirementname']}"
    else:
            alert_message = 'Record not found or already deleted.'
    conn.close()
    return redirect(url_for('managerequirement',alert=alert_message))

@app.route('/edit', methods=['POST'])
def edit():
    global recorddata
    global recordid
    global newstatus
    if request.method == 'POST':
    # Retrieve form data
        
        recordid = request.form['requirementid']
        requirementname = request.form['requirementname']
        clientname = request.form['clientname']
        clientmanager = request.form['clientmanager']
        departmentname = request.form['departmentname']
        accountmanager = request.form['accountmanager']
        jobdescription = request.form['jobdescription']
        workexperience = request.form['workexperience']
        openposition = request.form['openposition']
        timing = request.form['timing']
        locationname = request.form['locationname']
        workmode = request.form['workmode']
        recruiter = request.form['recruiter']
        budget = request.form['budget']
        comment = request.form['comment']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        display = request.form['display']
        status = request.form['status']
        app.logger.warning("A warning message."+requirementname) 
        newstatus =  request.form['status']
        recorddata = requirementname
    # Insert into database
        with get_db() as conn:
            curs = conn.cursor()
            curs.execute("UPDATE requirementdetail SET requirementname = ?, clientname = ?,clientmanager=?,departmentname=?,accountmanager=?,jobdescription=?,workexperience=?,openposition=?,timing=?,locationname=?,workmode=?,recruiter=?,budget=?,comment=?,startdate=?,enddate=?,display=?,status=? WHERE id = ?",
            (requirementname, clientname, clientmanager, departmentname, accountmanager, jobdescription,
              workexperience, openposition,timing,locationname,workmode,recruiter,budget,comment, startdate, enddate, display, status,recordid))
            conn.commit()
            if curs.rowcount > 0:
                alert_message = f"Record updated successfully! Requirement Name: {recorddata}"
                email_scheduler(currentstatus,newstatus)
            else:
                alert_message = 'Record not added. Requirement Name: {recorddata}'
               

            return redirect(url_for('managerequirement',alert=alert_message))
    else:
        with get_db() as conn:
            curs = conn.cursor()
            curs.execute('SELECT * FROM requirementdetail')
            requirements = curs.fetchall()
            return render_template('requirements.html',requirements=requirements)

@app.route('/redirect_page')
def redirect_page():
      return render_template('ctracker.html')

@app.route('/getreq/<int:record_id>', methods=['GET'])
def getreq(record_id):
            with get_db() as conn:
                curs = conn.cursor()
                curs.execute("SELECT * from requirementdetail WHERE id = ?", (record_id,))
                requirements = curs.fetchone()
                if requirements:
                    global currentstatus 
                    currentstatus = requirements['status']
                    return jsonify ({"id":requirements['id'],"requirementname":requirements['requirementname'],"clientname":requirements['clientname'],"clientmanager":requirements['clientmanager'],"departmentname":requirements['departmentname'],"accountmanager":requirements['accountmanager'],"jobdescription":requirements['jobdescription'],"workexperience":requirements['workexperience'],
                    "openposition":requirements['openposition'],"timing":requirements['timing'],"locationname":requirements['locationname'],"workmode":requirements['workmode'],"recruiter":requirements['recruiter'],"budget":requirements['budget'],"comment":requirements['comment'],"startdate":requirements['startdate'],"enddate":requirements['enddate'],"display":requirements['display'],"status":requirements['status']})

@app.route('/selectcolor', methods=['GET', 'POST'])
def selectcolor():
    selected_color = None
    
    if request.method == 'POST':
        selected_color = request.form.get('color')  # Get the selected color value
        session['background_color'] = selected_color
        with get_db() as conn:
            curs = conn.cursor()
            curs.execute('SELECT * FROM requirementdetail')
            requirements = curs.fetchall()
            return render_template('requirements.html',requirements=requirements)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    
