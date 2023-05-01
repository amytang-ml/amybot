# wikibot

## Install Dependancies
./install_pkg.sh

## code dirctory structure

wikiIndexer.py - class with methods to index wikipedia pages with certain LLM model and paraemters.
wikibot.py - implementation of wikibot, works for one wiki page at a time. form now.
static/chabot.js - javascript for wikibot web page
static/style.css - css style sheet for wikibot web page
templates/home.html - html template for wikibot web page
templatese/result.html - html template for wikibot web page

## Run wikibot

python3 wikibot.py -page "YOUR_PAGE_NAME"

# https://en.wikipedia.org/wiki/Indictment_of_Donald_Trump

the bot is hard coded to use the following LLM model and parameters
- page: Indictment_of_Donald_Trump
- model: text-davinci-003
- temperature: 0.3,  the higher the temperature, the more random the text, more likely to huluciante
