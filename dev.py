import requests

from datetime import datetime
from flask import Flask
from flask import render_template, redirect
from forms import MoneyForm
from db import StdPay, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hashlib import sha256

app = Flask(__name__, template_folder='../../templates/')
app.config['SECRET_KEY'] = 'my_secret_key'

engine = create_engine('postgresql+psycopg2://piastrix_USER:piastrix_PASS_[h5Z\wa3u-n`g?5B@postgres:5430/piastrix_DB')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

shop_id = '5'
secretKey = 'SecretKey01'
payway = "advcash_rub"


def make_bill(amount, shop_order_id, description):
    """when user choice USD currency: make sign and request payload url"""
    url = 'https://core.piastrix.com/bill/create'
    currency = 840  # USD
    hash_ = ':'.join([str(currency), str(amount), str(currency), shop_id, str(shop_order_id)]) + secretKey
    sign = sha256(hash_.encode())
    payload = {"payer_currency": currency,
               "shop_amount": amount,
               "shop_currency": currency,
               "shop_id": shop_id,
               "shop_order_id": shop_order_id,
               "sign": sign.hexdigest(),
               "description": description}
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url=url, json=payload, headers=headers)
    return response


def make_invoice(amount, shop_order_id):
    """when user choice RUB currency"""
    url = 'https://core.piastrix.com/invoice/create'
    currency = '643'  # RUB
    hash_ = ':'.join([str(amount), currency, payway, shop_id, str(shop_order_id)]) + secretKey
    sign = sha256(hash_.encode())
    payload = {"amount": str(amount),
               "currency": currency,
               "payway": payway,
               "shop_id": shop_id,
               "shop_order_id": str(shop_order_id),
               "sign": sign.hexdigest()}
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url=url, json=payload, headers=headers)
    return response


def this_is_the_way(currency, pay):
    """generate redirect in way to currency"""
    if currency == 'eur':
        hash_ = ':'.join([str(pay.amount), '978', shop_id, str(pay.shop_order_id)]) + secretKey
        sign = sha256(hash_.encode())
        return render_template('pay.html', **{
            'amount': pay.amount,
            'currency': 978,
            'shop_id': shop_id,
            'sign': sign.hexdigest(),
            'shop_order_id': pay.shop_order_id,
            'description': pay.description,
        })
    elif currency == 'usd':
        response = make_bill(pay.amount, pay.shop_order_id, pay.description)  # function
        if response and response.json()['result']:
            pay.timestamp = response.json()['data']['created']
            pay.pay_sys_id = response.json()['data']['id']
            pay.shop_refund = response.json()['data']['shop_refund']
            session.commit()
            return redirect(response.json()['data']['url'])

    elif currency == 'rub':
        response = make_invoice(pay.amount, pay.shop_order_id)  # function
        if response and response.json()['result']:
            pay.timestamp = datetime.now()
            pay.pay_sys_id = response.json()['data']['id']
            pay.shop_refund = response.json()['data']['data']['ac_amount']
            session.commit()
        return render_template('invoice.html', **{
            'ac_account_email': response.json()['data']['data']['ac_account_email'],
            'ac_sci_name': response.json()['data']['data']['ac_sci_name'],
            'ac_amount': response.json()['data']['data']['ac_amount'],
            'ac_sub_merchant_url': response.json()['data']['data']['ac_sub_merchant_url'],
            'ac_sign': response.json()['data']['data']['ac_sign'],
            'ac_currency': 'RUR',
            'ac_order_id': response.json()['data']['data']['ac_order_id'],
        })


@app.route('/', methods=['POST', 'GET'])
def raw23():
    """main route"""
    form = MoneyForm()
    if form.validate_on_submit():
        pay = StdPay(amount=round(form.amount.data, 2),
                     currency=form.currency.data,
                     description=form.description.data)
        session.add(pay)
        session.commit()
        pay.shop_order_id = 10000000 + pay.id

        return this_is_the_way(form.currency.data, pay)  # main function

    return render_template('base.html', form=form)
