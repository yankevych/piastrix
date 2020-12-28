from flask_wtf import FlaskForm
from wtforms import TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired


class MoneyForm(FlaskForm):
    """field form to make validator in the back-end side"""
    amount = FloatField('Amount', validators=[DataRequired()])
    currency = SelectField('Currency', choices=[('eur', 'EUR'), ('usd', 'USD'), ('rub', 'RUB')])
    description = TextAreaField("Description", validators=[DataRequired()])





