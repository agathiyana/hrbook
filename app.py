import sqlite3
from flask import  Flask, flash, jsonify, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

DATABASE = 'requirements.db'

def get_db():
    """Returns a connection to the SQLite database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows access to columns by name
    return conn

def init_db():
    """Initialize the database with required table"""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS requirement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                requirementname TEXT NOT NULL,
                clientname TEXT NOT NULL,
                clientmanager TEXT NOT NULL,
                departmentname TEXT NOT NULL,
                accountmanager TEXT NOT NULL,
                jobdescription TEXT NOT NULL,
                workexperience TEXT NOT NULL,
                openposition INTEGER NOT NULL,
                startdate TEXT NOT NULL,
                enddate TEXT NOT NULL,
                display TEXT NOT NULL,
                status TEXT NOT NULL
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
            curs.execute('SELECT * FROM requirement')
            requirements = curs.fetchall()

            labels = [row[2] for row in requirements]
            counts = [row[8] for row in requirements]

    # Create a figure and axis
     fig, ax = plt.subplots()
     fig, ax = plt.subplots()
     ax.bar(labels, counts, color='skyblue')
     ax.set_xlabel('clientname')
     ax.set_ylabel('openposition')
     ax.set_title('Requirement Distribution')
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
    global recorddata
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
            INSERT INTO requirement (requirementname, clientname, clientmanager, departmentname, accountmanager,
                                    jobdescription, workexperience, openposition, startdate, enddate, display, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (requirementname, clientname, clientmanager, departmentname, accountmanager, jobdescription,
              workexperience, openposition, startdate, enddate, display, status))
            conn.commit()
            if curs.rowcount > 0:
                alert_message = f"Record added successfully! Requirement Name: {recorddata}"
            else:
                alert_message = 'Record not added. Requirement Name: {recorddata}'
            return redirect(url_for('managerequirement',alert=alert_message))
    else:
        with get_db() as conn:
            curs = conn.cursor()
            curs.execute('SELECT * FROM requirement')
            requirements = curs.fetchall()
            return render_template('requirements.html',requirements=requirements)

# Route to delete a record
@app.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    global recorddata
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT requirementname from requirement WHERE id = ?", (record_id,))
    recorddata = cur.fetchone()
    # DELETE query to remove the record with the given ID
    cur.execute("DELETE FROM requirement WHERE id = ?", (record_id,))
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
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        display = request.form['display']
        status = request.form['status']
        app.logger.warning("A warning message."+requirementname)  
        recorddata = requirementname
    # Insert into database
        with get_db() as conn:
            curs = conn.cursor()
            curs.execute("UPDATE requirement SET requirementname = ?, clientname = ?,clientmanager=?,departmentname=?,accountmanager=?,jobdescription=?,workexperience=?,openposition=?,startdate=?,enddate=?,display=?,status=? WHERE id = ?",
            (requirementname, clientname, clientmanager, departmentname, accountmanager, jobdescription,
              workexperience, openposition, startdate, enddate, display, status,recordid))
            conn.commit()
            if curs.rowcount > 0:
                alert_message = f"Record updated successfully! Requirement Name: {recorddata}"
            else:
                alert_message = 'Record not added. Requirement Name: {recorddata}'
            return redirect(url_for('managerequirement',alert=alert_message))
    else:
        with get_db() as conn:
            curs = conn.cursor()
            curs.execute('SELECT * FROM requirement')
            requirements = curs.fetchall()
            return render_template('requirements.html',requirements=requirements)

@app.route('/redirect_page')
def redirect_page():
      return render_template('ctracker.html')

@app.route('/getreq/<int:record_id>', methods=['GET'])
def getreq(record_id):
            with get_db() as conn:
                curs = conn.cursor()
                curs.execute("SELECT * from requirement WHERE id = ?", (record_id,))
                requirements = curs.fetchone()
                if requirements:
                    return jsonify ({"id":requirements['id'],"requirementname":requirements['requirementname'],"clientname":requirements['clientname'],"clientmanager":requirements['clientmanager'],"departmentname":requirements['departmentname'],"accountmanager":requirements['accountmanager'],"jobdescription":requirements['jobdescription'],"workexperience":requirements['workexperience'],
                    "openposition":requirements['openposition'],"startdate":requirements['startdate'],"enddate":requirements['enddate'],"display":requirements['display'],"status":requirements['status']})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    
