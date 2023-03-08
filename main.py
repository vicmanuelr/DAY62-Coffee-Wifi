from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    name = StringField(label='Cafe name', validators=[DataRequired()])
    # Exercise:
    # add: Location URL, open time, closing time, coffee rating, Wi-Fi rating, power outlet rating fields
    location = URLField(label='Cafe Location on Google Maps (URL)', validators=[URL(), DataRequired()])
    # make coffee/Wi-Fi/power a select element with choice of 0 to 5.
    open = StringField(label='Opening Time e.g. 8AM', validators=[DataRequired()])
    closing = StringField(label='Closing Time e.g. 8PM', validators=[DataRequired()])
    cafe_selectors = ['☕️' * i for i in range(1, 6)]
    cafe_selectors.insert(0, '✘')
    cafe = SelectField(label='Coffee Rating', choices=cafe_selectors, validators=[DataRequired()])
    wifi_selectors = ['💪' * i for i in range(1, 6)]
    wifi_selectors.insert(0, '✘')
    wifi = SelectField(label='Wifi Strength', choices=wifi_selectors, validators=[DataRequired()])
    energy_selectors = ['🔌' * i for i in range(1, 6)]
    energy_selectors.insert(0, '✘')
    energy = SelectField(label='Energy Rating', choices=energy_selectors, validators=[DataRequired()])
    # e.g. You could use emojis ☕️/💪/✘/🔌
    # make all fields required except submit
    # use a validator to check that the URL field has a URL entered.
    # ---------------------------------------------------------------------------
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        new_line_data = form.data
        new_line = [item for key, item in new_line_data.items()]
        new_line = new_line[:-2]
        with open('cafe-data.csv', 'a') as f:
            i = 0
            for element in new_line:
                f.write(element)
                if i != 6:
                    f.write(",")
                i += 1
        return redirect(url_for("cafes"))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]
        headers = list_of_rows[0]
        content = list_of_rows[1::]
    return render_template('cafes.html', cafes=content, headers=headers)


if __name__ == '__main__':
    app.run(debug=True)
