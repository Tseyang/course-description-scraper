# Course Description Scraper (python3.6)
Just a derivative of other scripts that scrape Portal, it allows you to get course descriptions via course code through terminal without having to click through stuff on the webpage. I'm just too lazy to click through portal for descriptions while using [HyperScheduler](https://Hyperschedule.io).

# Usage
```
python course-info.py <Course Code> [Campus]
```
*Course Code* should be without campus or section e.g. "CSCI140" or "MATH131" or "PSYC189K". Certain course codes might use a space in between the faculty and course number i.e. enter into terminal as "Lit\ 99A"
*Campus* is optional and should be in the shortform that portal uses i.e. "HM", "CM", "SC", "PZ", "PO" or "CGU". Will search all campuses if left blank.

# Dependencies
## pip (for installing libraries)
```
easy_install pip  
```
## Selenium Webdriver
```
pip install selenium
```
I included the chromedriver in the repo for convenience.

## BeautifulSoup
```
pip install BeautifulSoup4
pip install lxml
```
