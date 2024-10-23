from flask_pymongo import PyMongo
from flask import *
app = Flask(__name__)
# connecting to the database
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/job_db")
# stores job details
db = mongodb_client.db
mongodb_client2 = PyMongo(app, uri="mongodb://localhost:27017/ppl_db")
# stores applicant details
db2 = mongodb_client2.db
print(db)
jobRole = ""
delret = None
# index page
@app.route('/')
def disp():
    return render_template("option.html")
# options page
@app.route('/optionApp', methods=["GET", "POST"])
def opt():
    apply = request.form['apply']
    if apply == "":
        return render_template("option.html", msg="Please choose an option")
    elif apply == "Apply":
        return render_template("home.html")
    return render_template("sorry.html")
# apply page
@app.route('/chooseJob', methods=["GET", "POST"])
def chooseJob():
    job = request.form["job"]
    global jobRole
    if job == "":
        return render_template("home.html", msg="Please choose a role")
    else:
        documents = db.job_col.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in 
        documents]
        ret = db.job_col.find_one({job: {"$gt": 0}})
        if ret is None:
            return render_template("home.html", msg="This role is not available")
        for i in range(5):
            for j in output[i]:
                if j == job:
                    print(output[i][j])
                    val = output[i][j] - 1
                    print(ret)
                    print(job, val)
                    jobRole = job
                    ret = db.job_col.update_one({job: {"$gt": 0}}, {"$set": {job: val}})
                    return render_template("getJob.html", msg="")
        return render_template("sorry.html")
# gets applicant details
@app.route('/congratulations', methods=["GET", "POST"])
def cong():
    msg = ""
    name = request.form["name"]
    a = request.form["age"]
    if a == "":
        age = -1
    else:
        age = int(a)
        gender = request.form.getlist("gender")
    if name == "":
        msg += "Please enter your name\n"
    if age < 0:
        msg += "Please enter your age\n"
    if age < 18:
        msg += "You are underage\n"
    if len(gender) == 0:
        msg += "Please enter your gender\n"
    if msg != "":
        return render_template("getJob.html", msg=msg)
    res = mongodb_client2.db.ppl_col.insert_one({'Name': name, 'Age': age, 'Gender': gender, 'Job': jobRole})
    print(res)
    return render_template("cong.html")
# removes applicant
@app.route('/enterDet', methods=['GET', 'POST'])
def enter():
    global delret
    name = request.form['name']
    if name == "":
        return render_template("sorry.html", msg="Please provide your name")
    delret = mongodb_client2.db.ppl_col.find_one({'Name': name})
    if delret is None:
        return render_template("sorry.html", msg='Applicant does not exist', 
    n="", a="", g="", job="", msg2="")
    print(delret)
    name = delret['Name']
    age = delret['Age']
    gender = delret['Gender'][0]
    job = delret['Job']
    return render_template("sorry.html", msg="Applicant exists", n=name, a=age, g=gender, job=job, msg2="")
# deletes from database
@app.route('/confirm', methods=['GET', 'POST'])
def conf():
    global delret
    if delret is None:
        return render_template("sorry.html", msg="", n="", a="", g="", job="", msg2="Unsuccessful!")
    name = delret['Name']
    print(delret['Name'])
    # ret = mongodb_client2.db.ppl_col.find_one({'Name': name})
    # print(ret)
    if delret is None:
        return render_template("sorry.html", msg="", n="", a="", g="", job="", msg2="Unsuccessful!")
    mongodb_client2.db.ppl_col.delete_one({'_id': delret['_id']})
    documents = db.job_col.find()
    output = [{item: data[item] for item in data if item != '_id'} for data in 
    documents]
    job = delret['Job']
    ret = db.job_col.find_one({job: {"$lte": 5}})
    if ret is None:
        return render_template("sorry.html", msg="", n="", a="", g="", job="", msg2="Unsuccessful!")
    for i in range(5):
        for j in output[i]:
            if j == job:
                print(output[i][j])
        val = output[i][j] + 1
        print(ret)
        print(job, val)
        ret = mongodb_client.db.job_col.update_one({job: {"$lte": 5}}, {"$set": {job: val}})
        print(ret)
        delret = None
        return render_template("sorry.html", msg="", n="", a="", g="", job="", msg2="Done!")
    return render_template("sorry.html", msg="", n="", a="", g="", job="", msg2="Unsuccessful!")
if __name__ == '__main__':
 app.run(debug=True)
