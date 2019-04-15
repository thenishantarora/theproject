import os
from flask import Flask
from flask import render_template
from flask import request, redirect
from pymongo import MongoClient
from fpdf import FPDF
import webbrowser
from values import L1,L2,L3,L4,L5,R1,R2,R3,R4,R5
import matplotlib.pyplot as plt
import numpy as np

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Report", ln=1, align="C")
pdf.image("fp.png", x = None, y = None, w = 0, h = 0, type = '', link = 'fp.png')

label = ['L1','L2','L3','L4','L5','R1','R2','R3','R4','R5']

client = MongoClient('localhost:27017')
db = client.FormData

app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# PEOPLE_FOLDER = os.path.join('static')
# app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def hello_world():
    return render_template('fp.html')

@app.route('/back', methods = ['POST'])
def back():
	return render_template('fp.html')

@app.route('/signup', methods = ['POST'])
def signup():
    # email = request.form['email']
    # email_addresses.append(email)
    name = request.form['name']
    father = request.form['father']
    dob = request.form['dob']
    address = request.form['address']
    phone = request.form['phone']
    counsellor = request.form['counsellor']

    l1rc = int(request.form['l1rc'])
    l2rc = int(request.form['l2rc'])
    l3rc = int(request.form['l3rc'])
    l4rc = int(request.form['l4rc'])
    l5rc = int(request.form['l5rc'])
    r1rc = int(request.form['r1rc'])
    r2rc = int(request.form['r2rc'])
    r3rc = int(request.form['r3rc'])
    r4rc = int(request.form['r4rc'])
    r5rc = int(request.form['r5rc'])

    l1p = request.form['l1p']
    l2p = request.form['l2p']
    l3p = request.form['l3p']
    l4p = request.form['l4p']
    l5p = request.form['l5p']
    r1p = request.form['r1p']
    r2p = request.form['r2p']
    r3p = request.form['r3p']
    r4p = request.form['r4p']
    r5p = request.form['r5p']

    L1_value = l1rc*L1[l1p]
    L2_value = l2rc*L2[l2p]
    L3_value = l3rc*L3[l3p]
    L4_value = l4rc*L4[l4p]
    L5_value = l5rc*L5[l5p]
    R1_value = r1rc*R1[r1p]
    R2_value = r2rc*R2[r2p]
    R3_value = r3rc*R1[r3p]
    R4_value = r4rc*R4[r4p]
    R5_value = r5rc*R5[r5p]

    sum = L1_value+L2_value+L3_value+L4_value+L5_value+R1_value+R2_value+R3_value+R4_value+R5_value

    percentages = []
    percentages.append(L1_value/sum)
    percentages.append(L2_value/sum)
    percentages.append(L3_value/sum)
    percentages.append(L4_value/sum)
    percentages.append(L5_value/sum)
    percentages.append(R1_value/sum)
    percentages.append(R2_value/sum)
    percentages.append(R3_value/sum)
    percentages.append(R4_value/sum)
    percentages.append(R5_value/sum)

    right_brain = (percentages[0]+percentages[1]+percentages[2]+percentages[3]+percentages[4])*100.0
    left_brain = 100.0 - right_brain 

    fig = plt.figure(figsize=(7, 7))
    index = np.arange(len(label))
    plt.bar(index, percentages)
    plt.xlabel('Fingerprint input', fontsize=15)
    plt.ylabel('Percentage', fontsize=15)
    plt.xticks(index, label, fontsize=15, rotation=30)
    plt.title('Innate Multiple Intelligencies for '+name,fontsize=20)
    plt.plot(range(1)) #plot exampl
    plt.savefig(name+'.png',dpi=fig.dpi)

    for x in percentages:
    	print (x)
    	# y=y+x

    # print(y)	



    # print(phone)

    db.mydb.insert_one(
        {
            # "ID": db.form.count() + 1,
            "name": name,
            "father's name": father,
            "date of birth": dob,
            "address": address,
            "phone": phone,
            "counsellor": counsellor,
            # "isActive": True
            # "date": date,
            # "time": time
        }
        )
    pdf.cell(200, 10, txt="Name : "+name, ln=1, align="L")
    pdf.cell(200, 10, txt="Father's name : " +father, ln=1, align="L")
    pdf.cell(200, 10, txt="Date of birth : " +dob, ln=1, align="L")
    pdf.cell(200, 10, txt="Address : "+ address, ln=1, align="L")
    pdf.cell(200, 10, txt="Phone : "+ phone, ln=1, align="L")
    pdf.cell(200, 10, txt="Counsellor's name : "+ counsellor, ln=1, align="L")

    nm = name+'.png'
    pdf.image(nm, x = None, y = None, w = 100, h = 100, type = '', link = nm)

    pdf.output(name +".pdf")            
    return render_template('reportgenerated.html')

if __name__ == '__main__':
    # app.run()  
    webbrowser.open_new_tab('http://127.0.0.1:5000/')
    app.run()  

     

# webbrowser.open_new_tab('http://127.0.0.1:5000/')
