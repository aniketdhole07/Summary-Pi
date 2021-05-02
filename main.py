from flask import Flask, render_template,request
import requests 
from werkzeug import secure_filename
import datetime
import pdftotext
app = Flask(__name__)  
main_url="http://2b69c45fce84.ngrok.io" 
@app.route("/")
def hello(): 
   return render_template('main.html')  

@app.route('/upload', methods = ['POST', 'GET'])
def upload(): 
    if request.method == 'POST':
        f = request.files['File']
        f.save(secure_filename("tmp.pdf"))
        
        with open("tmp.pdf", "rb") as f:
            pdf = pdftotext.PDF(f)
        print(len(pdf))
        all_pg=''
        pg_cnt=0
        for page in pdf:
            if(pg_cnt>2): 
                break
            pg_cnt+=1
            all_pg+=page
        res = requests.post(main_url+'/sum_txt', json={"ip_txt":all_pg})
        if res.ok:
            print(res.json())
    
        templateData = {
          'summary'  : res.json()["summary"] 
          }
        return render_template('main.html', **templateData)
 
@app.route('/txt',methods= ['POST' , 'GET'])
def txt():
    if request.method == 'POST':
        ip_txt = request.form.get("Text") 
        print("a",ip_txt)
        res = requests.post(main_url+'/sum_txt', json={"ip_txt":ip_txt})
        if res.ok:
            print(res.json())
        templateData = {
          'summary' : res.json()["summary"]
          }
        return render_template('main.html', **templateData)
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

