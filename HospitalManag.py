from flask import Flask, render_template,request,session
from flask_session import Session

import sqlite3

from werkzeug.utils import redirect

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

connection = sqlite3.connect("hospitalmanagement.db", check_same_thread=False)

listOfTables1 = connection.execute("SELECT name from sqlite_master WHERE type='table' AND name='Patient' ").fetchall()

if listOfTables1!=[]:
   print("Sorry entered table is available!")
else:
    connection.execute(''' CREATE TABLE PATIENT1(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientNAME TEXT,
    PatientSurname TEXT,
    DiseaseCATEGORY TEXT,
    address TEXT,
    PPASSWORD TEXT
    manager TEXT); ''')
    print("Congratulations! Table creation done successfully!")

listOfTables2 = connection.execute("SELECT name from sqlite_master WHERE type='table' ").fetchall()

if listOfTables2!=[]:
   print("Table available already!")
else:
    connection.execute(''' CREATE TABLE Patient1(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PNAME TEXT,
    PSurname TEXT,
    PDisease TEXT,
    PBill TEXT,
    PManager TEXT); ''')
    print("Table creation done sucessfully")

cursor = connection.cursor()
cursor.execute("SELECT PName,PBILL FROM Patient")
ressult = cursor.fetchall()
print(ressult)


@app.route("/")
def myhome():
    return render_template("WebHome.html")


@app.route("/managerloginpanel", methods=["GET", "POST"])
def allogin():
    if request.method == "POST":
        getUname = request.form["username"]
        getppass = request.form["password"]

        if getUname == "Mr.Blacksmith":
            if getppass == "Piyush@123":
                return redirect("/patiententry")
    return render_template("ManagementLoginForm.html")


@app.route("/patiententry", methods=["GET", "POST"])
def patiententry():
    if request.method == "POST":
        getPatientName = request.form["name"]
        getSurname = request.form["surname"]
        getDiseasey = request.form["disease"]
        getBill = request.form["bill"]
        getManager = request.form["manager"]
        print(getPatientName)
        print(getSurname)
        print(getDiseasey)
        print(getBill)
        print(getManager)
        try:
            connection.execute("INSERT INTO PATIENT(PatientName,Surname,Diseasey,Bill,Manager) VALUES('"+getPatientName+"','"+getSurname+"','"+getDiseasey+"','" +getBill+"','"+getManager+"')")
            print("Congratulations! Patient data inserted sucessfully !")
            connection.commit()
            return redirect("/ViewAllPatient")
        except Exception as e:
            print(e)
    return render_template("PatientEntry.html")


@app.route("/patientsearch", methods=["GET", "POST"])
def patientsearch():
    if request.method == "POST":
        getPatientName = request.form["pname"]
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BOOKS WHERE PatientName = '"+getPatientName+"' ")
        ressultset = cursor.fetchall()
        return render_template("ViewAllPatient.html", bookss=res2)
    return render_template("PatientSearch.html")


@app.route("/patientinfoedit", methods=["GET","POST"])
def patientinfoedit():
    if request.method == "POST":
        getNewname = request.form["NewPatient"]
        getNewSurname = request.form["NewSurname"]
        getNewDisease = request.form["NewDisease"]
        getNewBill = request.form["NewBill"]
        getNewManager = request.form["NewManager"]
        connection.execute("UPDATE Patient SET Patient = '"+getNewname+"',AUTHOR = '"+getNewSurname+"',CATEGORY ='"+getNewDisease+"',PRICE = '"+getNewBill+"',PUBLISHER = '"+getNewManager+"'  ")
        print("Patient Information Updataed Sucessfully!")
        connection.commit()
        return redirect("/viewallpatient")
    return render_template("PatientDetailsEdit.html")


@app.route("/patientinfodelete", methods=["GET", "POST"])
def patientinfodelete():
    if request.method == "POST":
        getNAMEDEL = request.form["namedel"]
        cursorr = connection.cursor()
        cursorr.execute("DELETE FROM Patient WHERE PatientName = '"+getNAMEDEL+"' ")
    return render_template("PatientDelete.html")


@app.route("/viewallpatient")
def viewallpatient():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PATIENT")
    resultset = cursor.fetchall()
    return render_template("ViewAllPatient.html", bookss=res)





@app.route("/managementregistration", methods=["GET", "POST"])
def Managementregistration():
    if request.method == "POST":
        getPname = request.form["pname"]
        getPSurname= request.form["psurname"]
        getDisease = request.form["pdisease"]
        getbill= request.form["pbill"]
        getaddress = request.form["paddress"]
        connection.execute("INSERT INTO patient(PNAME, PSURNAME,DISEASE,BILL,ADDRESS) VALUES('" + getPname + "','" + getPSurname + "','" + getDisease + "','" + getbill + "','" + getaddress + "')")
        print("successfully inserted !")
        connection.commit()
        return redirect("/managerprofilelogin")
    return render_template("ManagementRegistrationForm.html")


@app.route("/patientprofileview")
def patientprofileview():
    if not session.get("name"):
        return redirect("/userprofilelogin")
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM PATIENT")
        result = cursor.fetchall()
        return render_template("PatientView.html", bookss=result)


@app.route("/managerprofilelogin", methods=["GET", "POST"])
def managerprofilelogin():
    if request.method == "POST":
        getuseremail = request.form["Uname"]
        getuserpass = request.form["Upass"]
        print(getuseremail)
        print(getuserpass)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Patient WHERE PNAME = '"+getuseremail+"' AND PPASSWORD = '"+getuserpass+"'")
        ressult = cursor.fetchall()
        if len(ressult) > 0:
            for i in ressult:
                getName = i[1]
                getid = i[0]

            session["name"] = getName
            session["id"] = getid

            return redirect("/patientview")
    return render_template("ManagementLoginForm.html")


@app.route("/patientprofilesearch", methods=["GET", "POST"])
def patientprofilesearch():
    if not session.get("name"):
        return redirect("/managerprofilelogin")
    else:
        if request.method == "POST":
            getpName = request.form["pbname"]
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Patient WHERE PNAME = '" + getpName + "' ")
            ressult= cur2.fetchall()
            return render_template("PatientProfileView.html", bookss=res2)
        return render_template("PatientProfileSearch.html")


@app.route("/managementlogoutform", methods=["GET", "POST"])
def managementlogoutform():

    if not session.get("name"):
        return redirect("/managementprofilelogin")
    else:
        session["name"] = None
        return redirect("/")


if __name__ == "__main__":
    app.run()