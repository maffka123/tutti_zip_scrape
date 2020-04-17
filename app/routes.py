from app import app
from app import scrape_tutti
from flask import render_template, url_for, request, redirect, flash, session


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    kanton_list = 'Ganze-Schweiz, Zürich, Bern, Luzern, Uri, Schwyz, Nid-Obwalden, Glarus, Zug, Freiburg, \
     Solothurn, Basel, Schaffhausen, Appenzell, St-gallen, Graubünden,Aargau, Thurgau, \
        Ticino, Vaud, Liechtenstein, Wallis, Neuenburg, Genf, Jura'
    kanton_list = kanton_list.split(', ')
    zip = None
    price_min = None
    price_max = None
    searching_for = None
    final_ads = []
    kanton='Ganze-Schweiz'

    if request.method == 'POST':
        select = request.form.get('kanton_list')
        if select is not None:
            kanton = select


        select = request.form.get('zip')
        if select is not None:
            zip=select
            print(zip)

        select = request.form.get('price_min')
        if select is not None:
            price_min=select

        select = request.form.get('price_max')
        if select is not None:
            price_max=select

        select = request.form.get('searching_for')
        if select is not None:
            searching_for=select
            print(searching_for)

        select = request.form.get('Los')
        if select is not None:
            final_ads=scrape_tutti.main(zip, kanton=kanton, price_min=price_min,
                                        price_max=price_max, searching_for=searching_for, in_app=True)


        kanton_list.remove(kanton)
        kanton_list.insert(0, kanton)

    return render_template('index.html',
                           final_ads = final_ads,
                           kanton_list=kanton_list,
                           )