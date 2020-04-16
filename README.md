## Filter tutti.ch search results by ZIP code

Unfortunately tutt.ch does not have ability to filter search results based on the ZIP. It can be however important if you are searching for something heavy and don't have a car (like me).

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
chmod +x ./scrape_tutti.py
./scrape_tutti.py --zip=your_zip --city=your_city --price_min=min_price --price_max=max_price --searching_for=what_do_you_want
```

All options except zip are optional

### 2. How does it work

Every search in tutti.ch is defined in the link, I insert all search options into the link and use bs4 to get the result, then parse the page to find needed zips.
