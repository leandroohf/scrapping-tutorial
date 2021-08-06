# Scrapy Tutorial Starter

Starter project for scrapy tutorial at https://github.com/harrywang/scrapy-tutorial
https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0

## Setup

Tested with Python 3.6 via virtual environment:
```shell
$ python3.6 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```


# How to run spiders


```shell
# run spider
 scrapy crawl quotes

# save output in json 
scrapy crawl quotes -o quotes.json
 
```
