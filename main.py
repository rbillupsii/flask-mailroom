import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation 

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    
@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':
        query = Donor.select().where(Donor.name == request.form['name'])
        if query.exists():
            donor = query.get()
        else:
            donor = Donor(name=request.form['name'])
            donor.save()

        donation = Donation(donor=donor, value=request.form['amt'])
        donation.save()

        return redirect(url_for('all'))
    else:
        return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

