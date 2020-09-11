# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 11:00:16 2020

@author: Prasun Biswas
"""

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def check(email):
    url = "https://kuerv9ukrh.execute-api.us-east-2.amazonaws.com/plasmanew/getdata?email="+email
    status = requests.request("GET",url)
    print(status.json())
    return status.json()


@app.route('/registration')
def home():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    x = [x for x in request.form.values()]
    print(x)
    params = "name="+x[0]+"&email="+x[1]+"&phone="+x[2]+"&city="+x[3]+"&infect="+x[4]+"&Blood="+x[5]+"&password="+x[6]
    
    if('errorType' in check(x[1])):
        url = "https://kuerv9ukrh.execute-api.us-east-2.amazonaws.com/plasmanew/registration?"+params
        response = requests.get(url)
        return render_template('register.html', pred="Registration Successful, please login using your details")
    else:
        return render_template('register.html', pred="You are already a member, please login using your details")

@app.route('/')    
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/loginpage',methods=['POST'])
def loginpage():
    user = request.form['user']
    passw = request.form['passw']
    print(user,passw)
    data = check(user)
    if('errorType' in data):
        return render_template('login.html', pred="The username is not found, recheck the spelling or please register.")
    else:
        if(passw==data['password']):
            return redirect(url_for('stats'))
        else:
            return render_template('login.html', pred="Login unsuccessful. You have entered the wrong password.") 
        
        
@app.route('/stats')
def stats():
    url = "https://kuerv9ukrh.execute-api.us-east-2.amazonaws.com/plasmanew/getbloodgroupsdata"
    response = requests.request("GET",url)
    r = response.json()
    print(r)
    return render_template('stats.html',b=sum(r),b1=str(r[0]),b2=str(r[1]),b3=str(r[2]),b4=str(r[3]),b5=str(r[4]),b6=str(r[5]),b7=str(r[6]),b8=str(r[7]))

@app.route('/requester')
def requester():
    return render_template('request.html')


@app.route('/requested',methods=['POST'])
def requested():
    bloodgrp = request.form['bloodgrp']
    #print(bloodgrp)
    url = "https://kuerv9ukrh.execute-api.us-east-2.amazonaws.com/plasmanew/bloodrequest?Blood="+bloodgrp
    status = requests.request("GET",url)
    a=status.json()
    #email=[]
    phone=[]
    for i in a:
        url= "https://www.fast2sms.com/dev/bulk?authorization=AT5p1bgOGwclB2fIF9W6kEPZqiQavHdoDJ7Sj0ruthUNYL8CsVijWGOHBpNftVvISDgxKMmXLl4FoPsJ&sender_id=FSTSMS&message=Need Plasma of Blood group&language=english&route=p&numbers="+str(i['phone'])
        #email.append(i['email'])
        result=requests.request("GET",url)
        print(result)
        phone.append(i['phone'])
    #print(email)
    print(phone)
    return render_template('request.html', pred="Your request is sent to the concerned people.")
    

if __name__ == "__main__":
    #app.run(host='0.0.0.0',port=5000)
    app.run(debug=True)

