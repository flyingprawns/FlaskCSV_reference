from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    opening = StringField('Open time (example: 9AM)', validators=[DataRequired()])
    closing = StringField('Close time (example: 3:30PM)', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', choices=['✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'])
    wifi = SelectField('Wifi Rating', choices=['✘', '📶', '📶📶', '📶📶📶', '📶📶📶📶', '📶📶📶📶📶'])
    power = SelectField('Power outlet Rating', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Add form data to cafes-data.csv
        with open('cafe-data.csv', 'a', encoding="utf8", newline='') as csv_file:
            csv_file.write('\n')
            csv_file.write(form.cafe.data)
            csv_file.write(',')
            csv_file.write(form.location.data)
            csv_file.write(',')
            csv_file.write(form.opening.data)
            csv_file.write(',')
            csv_file.write(form.closing.data)
            csv_file.write(',')
            csv_file.write(form.coffee.data)
            csv_file.write(',')
            csv_file.write(form.wifi.data)
            csv_file.write(',')
            csv_file.write(form.power.data)

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    # Read cafe data
    with open('cafe-data.csv', encoding="utf8", newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
