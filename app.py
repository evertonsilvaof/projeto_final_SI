# save this as app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def olá():
   # return '<h1>Olá, mundo!</h1>'
   return render_template('index.html')

@app.route("/equipe.html")
def equipe():
   # return '<h1>Olá, mundo!</h1>'
   return render_template('equipe.html')




app.run()