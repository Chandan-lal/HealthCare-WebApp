from flask import Flask,render_template,request
import pickle
import mysql.connector

app = Flask(__name__)

username = []
update_email = []
fetch_email = []
model = pickle.load(open('model_chandan.pkl','rb'))

@app.route("/")
def index():
     return render_template("main_home_page.html") #to send context to html

@app.route('/test_page')
def test_page():
     return render_template("chandan.html")
@app.route('/predict', methods = ['POST','GET'])
def predict():
     l = []
     for x in request.form.values():
          l.append(int(x))

     print(l)

     l = [l]
     prediction = model.predict(l)
     conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
     cursor = conn.cursor()
     sql = "UPDATE users SET Disease = %s WHERE Email = %s "
     val = (prediction[0], username[0])
     cursor.execute(sql, val)
     conn.commit()
     cursor.close()
     conn.close()

     return render_template("congrats_page.html", pred = prediction[0])



@app.route('/prescription')
def prescription():
    conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
    cursor = conn.cursor()
    sq = """select * from users"""
    cursor.execute(sq)
    records = cursor.fetchall()
    for i in records:
        if username[0] == i[0]:
            a1 = i[6]
            a2 = i[7]
            a3 = i[9]
            break
    if len(a1) == 0:
        return render_template("user_menu.html", s = "You need to take test first !")
    else:
        return render_template("medication_details_page.html", pred4 = a1, pred5 = a2, pred6 = a3)

@app.route('/order_page')
def order_page():
    conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
    cursor = conn.cursor()
    sq = """select * from users"""
    cursor.execute(sq)
    records = cursor.fetchall()
    for i in records:
        if username[0] == i[0]:
            a1 = i[7]
            a2 = i[8]

            break

    l1=a1.split()
    l2 = a2.split()
    l3=[]
    x=0
    for i in range(len(l2)):
        sum=len(l1[i])*int(l2[i])
        l3.append(sum)
        x+=int(sum)

    if len(l1)==1:
        return render_template("order_page.html", q1=l1[0],p1=l2[0],q6=x)
    elif len(l1)==2:
        return render_template("order_page.html",q1=l1[0],q2=l1[1],p1=l2[0],p2=l2[1],q6=x)
    elif len(l1)==3:
        return render_template("order_page.html",q1=l1[0],q2=l1[1],q3=l1[2],p1=l2[0],p2=l2[1],p3=l2[2],q6=x)
    elif len(l1)==4:
        return render_template("order_page.html",q1=l1[0],q2=l1[1],q3=l1[2],q4=l1[3],p1=l2[0],p2=l2[1],p3=l2[2],p4=l2[3],q6=x)
    elif len(l1)==5:
        return render_template("order_page.html",q1=l1[0],q2=l1[1],q3=l1[2],q4=l1[3],q5=l1[4],p1=l2[0],p2=l2[1],p3=l2[2],p4=l2[3],p5=l2[4],q6=x)

@app.route('/complete', methods = ['POST','GET'])
def complete():
    l = []
    for x in request.form.values():
        l.append(x)
    m = "Online"
    conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
    cursor = conn.cursor()
    sql = "UPDATE billing SET Name = %s, Phone = %s, Address = %s, City = %s, Mode = %s WHERE Email = %s "
    val = (l[0], l[1], l[2], l[3], m, username[0])
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()

    return render_template("user_menu.html",s="ordered successfully")

#User_page Done
@app.route('/index_func1')
def index_func1():
     return render_template("login_register.html")
@app.route('/login')
def login():
     return render_template("login_page.html")
@app.route('/register')
def register():
     return render_template("register_page.html")
@app.route('/login_verify', methods = ['POST','GET'])
def login_verify():
     k = []
     conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
     for x in request.form.values():
          k.append(x)
     username.clear()
     username.append(k[0])
     cursor = conn.cursor()
     sq = """select * from users"""
     cursor.execute(sq)
     records = cursor.fetchall()
     for i in records:
          if username[0] == i[0] and k[1] == i[1]:
               return render_template("user_menu.html")

     return render_template("login_page.html", pred1=" Wrong Credentials. Try Again !!!")

@app.route('/register_verify', methods = ['POST','GET'])
def register_verify():
    l = []
    conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
    for x in request.form.values():
        l.append(x)
    username.clear()
    username.append(l[0])
    cursor = conn.cursor()
    sq = """select * from users"""
    cursor.execute(sq)
    records = cursor.fetchall()
    for i in records:
        if username[0] == i[0]:
            return render_template('register_page.html', pred = "This Email already exists in Our Database")

    iquery = """insert into users (Email,Password,Name,DOB,Allergies,Ailments,Descriptions) values (%s,%s,%s,%s,%s,%s,%s)"""
    val = (l[0],l[1],l[3],l[4],l[5],l[6],'None')
    try:
        cursor.execute(iquery, val)
        conn.commit()
    except:
        conn.rollback()

    cursor.close()
    conn.close()

    return render_template("user_menu.html")
@app.route('/user_menu_page')
def user_menu_page():
     return render_template("user_menu.html")
@app.route("/user_update_func")
def user_update_func():
    return render_template("user_details_update.html")

@app.route("/user_update_form", methods = ['POST','GET'])
def  user_update_form():
    l = []
    for x in request.form.values():
        l.append(x)

    conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
    cursor = conn.cursor()
    sql = "UPDATE users SET Allergies = %s , Ailments= %s WHERE Email = %s "
    val = (l[0], l[1], username[0])
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()

    return render_template("user_menu.html")


#Doctor Page
@app.route('/index_func2')
def index_func2():
     return render_template("admin_page.html")
@app.route('/update')
def update():
     return render_template("update_page.html")
@app.route('/update_form_1', methods = ['POST','GET'])
def update_form_1():
    flag = 0
    update_email.clear()
    for x in request.form.values():
        update_email.append(x)
        break

    conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
    cursor = conn.cursor()
    sq = """select * from users"""
    cursor.execute(sq)
    records = cursor.fetchall()
    for i in records:
        if update_email[0] == i[0]:
            flag = 1
            a1 = i[2]
            a2 = i[3]
            a3 = i[4]
            a4 = i[5]
            a5 = i[6]
            break
    if flag == 1:
        return render_template("pres_page.html", pred1 = a1, pred2 = a2, pred3 = a3, pred4 = a4, pred5 = a5)
    else:
        return render_template("update_page.html", pred111 = "Wrong Email, Try Again !")
@app.route('/update_form_2', methods = ['POST','GET'])
def update_form_2():
     l = []
     for x in request.form.values():
          l.append(x)

     conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
     cursor = conn.cursor()
     sql = "UPDATE users SET Descriptions = %s, Quantity = %s, Timings_for_Doses = %s WHERE Email = %s "
     val = (l[0],l[1],l[2], update_email[0])
     cursor.execute(sql, val)
     conn.commit()
     cursor.close()
     conn.close()

     conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
     cursor = conn.cursor()
     iquery = """insert into billing (email,medicine,quantity) values (%s,%s,%s)"""
     val = (update_email[0], l[0], l[1])
     try:
         cursor.execute(iquery, val)
         conn.commit()
     except:
         conn.rollback()

     cursor.close()
     conn.close()

     return render_template("admin_page.html", pred3 = "Successfully Updated the Prescriptions")

#Pharm_page
@app.route('/index_func3')
def index_func3():
     return render_template("pharm_details.html")
@app.route('/customer_view_func', methods = ['POST','GET'])
def fetch_form_page():
    flag = 0
    fetch_email.clear()
    for x in request.form.values():
        fetch_email.append(x)
        break

    conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
    cursor = conn.cursor()
    sq = """select * from users"""
    cursor.execute(sq)
    records = cursor.fetchall()
    for i in records:
        if fetch_email[0] == i[0]:
            flag = 1
            k = i[0]
            k1 = i[2]
            l = i[3]
            m = i[7]
            n = i[8]
            o = i[9]
            break
    if flag == 1:
        return render_template('details_page.html', pred4=k, pred5 = k1, pred6 = l, pred7 = m, pred8 = n, pred9 = o)
    else:
        return render_template("pharm_details.html", pred111 = "Wrong Email, Try Again !")
@app.route('/back_func')
def back_func():
     return render_template("pharm_details.html")


#Online View Table
@app.route('/index_func4')
def index_func4():
    conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
    cursor = conn.cursor()
    sq = """select * from billing"""
    cursor.execute(sq)
    records = cursor.fetchall()

    return render_template("online_details.html", students = records)
@app.route('/index_func4_return')
def index_func4_return():
    return render_template("main_home_page.html")
@app.route('/issued_online')
def issued_online():
    return render_template("Issues_update_page.html")
@app.route('/Issue_update_form', methods = ['POST','GET'])
def Issue_update_form():
    flag=0
    for x in request.form.values():
        k=x
        break
    conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
    cursor = conn.cursor()
    sq = """select * from billing"""
    cursor.execute(sq)
    records = cursor.fetchall()
    for i in records:
        if k == i[0]:
            flag=1
    conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="chandan")
    cursor = conn.cursor()
    sql = "UPDATE billing SET issued = %s WHERE Email = %s "
    val = ("Yes", k)
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()

    return render_template("main_home_page.html")


@app.route('/logout_func')
def logout_func():
     return render_template("main_home_page.html")

if __name__ == "__main__":
     app.run(debug = True)