## Filter tutti.ch search results by ZIP code (Suchergebnisse von tutti.ch nach Postleitzahl filtern)

Unfortunately tutti.ch does not have ability to filter search results based on the ZIP. It can be however important if you are searching for something heavy and don't have a car (like me).

So I have wrote a simple script that scrapes tutti.ch

## How it works

### 1. Simple start from commandline

in command line type:

* create virtual environment and install requirements:

(for details: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash
python3.7 -m venv v
source v/bin/activate
pip install -r requirements.txt
```

* Make script executable and run it

```bash
cd app
chmod +x ./scrape_tutti.py #this is maybe not nesessary
python scrape_tutti.py --zip=your_zip --city=your_city --price_min=min_price --price_max=max_price --searching_for=what_do_you_want
```

All options except zip are optional:

- zip can be in form 8056, 805*, 80* or 805., 80. etc.

- city should have umlauts if there are some, or ue, ae, oe

- prices just a number

- searching for one word for now, it is enough for me :)

* Example:

```bash
python scrape_tutti.py --zip=80. --city=zuerich  --price_max=3 --searching_for=tisch
```

Will save .csv file and print the table:

### 3. Flask app serving

```bash
export FLASK_APP=scrape_tutti_inro.py 
flask run
```

Unfortunately does not show images, because they are renderred by Java and selenium does not work for me. Waiting when bugs will be fixed.

### 2. How does it work

Every search in tutti.ch is defined in the link, I insert all search options into the link and use bs4 to get the result, then parse the page to find needed zips.
