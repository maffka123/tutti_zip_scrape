from app import app
from app import scrape_tutti
from flask import render_template, url_for, request, redirect, flash, session
import logging

logging.basicConfig(filename='tutti.log', level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
logging.info('Starting')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    kanton_list = 'Ganze-Schweiz, Zürich, Bern, Luzern, Uri, Schwyz, Nid-Obwalden, Glarus, Zug, Freiburg, \
     Solothurn, Basel, Schaffhausen, Appenzell, St-gallen, Graubünden,Aargau, Thurgau, \
        Ticino, Vaud, Liechtenstein, Wallis, Neuenburg, Genf, Jura'
    kanton_list = kanton_list.split(', ')
    final_ads=[]
    form={'zip':None,
    'price_min': None,
    'price_max': None,
    'searching_for': None,
    'kanton':'Ganze-Schweiz'}


    if request.method == 'POST':

        form = check_form(form, session, request)
        logging.info('Search arameters were: '+ str(form))

        select = request.form.get('Los')
        if select is not None:
            try:
                final_ads=scrape_tutti.main(form['zip'], kanton=form['kanton'], price_min=form['price_min'],
                                        price_max=form['price_max'], searching_for=form['searching_for'], in_app=True)


            except:
                logging.error("Fatal error in main loop", exc_info=True)

        #Shuffle kantons in the list so it will show the chosen kanton
        kanton_list.remove(form['kanton'])
        kanton_list.insert(0, form['kanton'])

    return render_template('index.html',
                           final_ads=final_ads,
                           kanton_list=kanton_list,
                           zip=form['zip'],
                           price_min=form['price_min'],
                           price_max=form['price_max'],
                           )


def check_form(form, session, request):


    if 'kanton' in session:
        form['kanton'] = session['kanton']

    for f in ['kanton','zip','price_min','price_max','searching_for']:
        select = request.form.get(f)
        if select is not None:
            form[f] = select
            session[f] = select
        if f in session:
            form[f] = session[f]

    return form