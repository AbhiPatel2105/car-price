from flask import Flask
from flask import render_template,request
import pickle
from datetime import date




app = Flask(__name__)
model = pickle.load(open('car_prize_for_car_data.pkl','rb'))
@app.route('/')
def home():
    return render_template('car.html')

@app.route('/submit',methods = ['POST'])
def submit():
    if request.method == 'POST':
        year = int(request.form['year'])
        todays_date = date.today()
        current_year = todays_date.year
        no_of_year = current_year - year
        present_price = float(request.form['present_price'])
        kilometer_driven = int(request.form['kilometer_driven'])
        owner = int(request.form['owner'])
        fuel_type = str(request.form['fuel_type'])
        if fuel_type=='Petrol':
            fuel_type_petrol = 1
            fuel_type_diesel = 0
        elif fuel_type=='Diesel':
            fuel_type_petrol = 0
            fuel_type_diesel = 1
        else:
            fuel_type_petrol = 0
            fuel_type_diesel = 0
        seller_type = str(request.form['seller_type'])
        if seller_type=='Dealer':
            seller_type_individual=0
        else:
            seller_type_individual=1
        transmission = str(request.form['transmission'])
        if transmission=='Manual':
            transmission_manual = 1
        else:
            transmission_manual = 0
        prediction = model.predict([[present_price,kilometer_driven,owner,no_of_year,fuel_type_diesel,fuel_type_petrol,seller_type_individual,transmission_manual]])
        output=round(prediction[0],2)
        return render_template('car.html',prediction="your car can sell at {}".format(prediction) )
    else:
        return render_template('car.html',prediction='no prediction')



if __name__=="__main__":
    app.run(debug=True)
