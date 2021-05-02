from flask import Flask, render_template, jsonify,redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import date
  
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///treasury_yield_curve_rates.db'

db = SQLAlchemy(app)

class TreasuryYieldTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), nullable=False)
    one_mo = db.Column(db.String(255), nullable=False)
    two_mo = db.Column(db.Float, nullable=False)
    three_mo = db.Column(db.Float, nullable=False)
    six_month = db.Column(db.Float, nullable=False)
    one_year = db.Column(db.Float, nullable=False)
    two_year = db.Column(db.Float, nullable=False)
    three_year = db.Column(db.Float, nullable=False)
    five_year = db.Column(db.Float, nullable=False)
    seven_year = db.Column(db.Float, nullable=False)
    ten_year = db.Column(db.Float, nullable=False)
    twenty_year = db.Column(db.Float, nullable=False)
    thirty_year = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Treasury yield curve rates {self.id} {self.date}>"

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/charts/<chart>', methods = ['GET'])
def get_chart(chart):
    return send_file('charts/'+chart, mimetype = "image/png")

@app.route('/get_chart_today', methods = ['GET'])  
def get_chart_today():
    today = date.today()
    d = today.strftime("%m-%d-%y")
    return send_file(f'charts/test-{d}.png')
    
if __name__=='__main__':
    app.run(debug=True)