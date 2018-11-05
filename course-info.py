"""
Author: Tse Yang Lim
"""

import sys
import json
import selenium.webdriver
import selenium.webdriver.chrome.options
import selenium.webdriver.support.ui
from bs4 import BeautifulSoup
import json
import re

# Globals/Parameters
current_term = "FA"
portal_URL = ("https://portal.hmc.edu/ICS/Portal_Homepage.jnz?"
        "portlet=Course_Schedules&screen=Advanced+Course+Search"
        "&screenType=next")

# Exceptions
class ScrapeError(Exception):
    pass

def get_browser(headless):
    """
    desc: Creates Selenium Webdriver
    param: bool, whether to use a headless Selenium webbrowser or not
    ret: Selenium webdriver
    """
    opts = selenium.webdriver.chrome.options.Options()
    opts.set_headless(headless)
    opts.add_argument("--hide-scrollbars")
    browser = selenium.webdriver.Chrome(executable_path="./chromedriver", chrome_options=opts)
    return browser

def get_portal_html(browser, target, campus):
    """
    search portal for the target course
    """
    browser.get(portal_URL)
    term_dropdown = selenium.webdriver.support.ui.Select(browser.find_element_by_id("pg0_V_ddlTerm"))
    term_names = [option.text for option in term_dropdown.options]

    # find the most recent term in the catalogues i.e. term we are interested in
    terms = []
    for term_name in term_names:
        match = re.match(r"\s*(FA|SP)\s*([0-9]{4})\s*", term_name)
        if match:
            fall_or_spring, year_str = match.groups()
            terms.append((int(year_str), fall_or_spring == current_term, term_name))

    if not terms:
        raise ScrapeError("couldn't parse any term names (from: {})".format(repr(term_names)))

    most_recent_term = max(terms)

    # actually select the term in the dropdown
    term_dropdown.select_by_visible_text(most_recent_term[2])

    # add campus if given
    if campus:
        campus_dropdown = selenium.webdriver.support.ui.Select(browser.find_element_by_id("pg0_V_ddlCampus"))
        campus_dropdown.select_by_visible_text(campus + " Campus")
    else:
        campus_input = selenium.webdriver.support.ui.Select(browser.find_element_by_id("pg0_V_ddlCampus"))
        campus_input.select_by_visible_text("All")

    # input course code
    course_code_field = browser.find_element_by_id("pg0_V_txtCourseRestrictor")
    course_code_field.clear()
    course_code_field.send_keys(target)

    # search
    search_button = browser.find_element_by_id("pg0_V_btnSearch")
    search_button.click()

    return browser.page_source

def find_desc_from_portal_html(html, target, browser):
    """
    goes to the target course page from the search results page
    """
    soup = BeautifulSoup(html, "lxml")

    # strip out course listings from portal table rows
    table = soup.find(id="pg0_V_dgCourses")
    if not table:
        print("Could not find course code")
        exit(0)

    # assume first valid course code is the one we are looking for
    target_course = browser.find_element_by_id("pg0_V_dgCourses_sec2_row2_lnkCourse")
    target_course.click()

    notes = browser.find_element_by_id("pg0_V_lblNotesValue").text
    notes = notes[:notes.find("Eligible to register?")]
    desc = browser.find_element_by_id("pg0_V_lblCourseDescValue").text

    return notes + "\n" + desc

if __name__ == "__main__":
    print("It is assumed that the section of this course does not change the description.\n")
    browser = get_browser(True)
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Input in the form: python course-info.py <Course Code> [Campus], where <Course Code> does not contain the campus or the section and [Campus] is optional and contains the campus shortform e.g. \"HM\"")
        exit(0)
    target = sys.argv[1]
    campus = sys.argv[2] if len(sys.argv) == 3 else None
    if campus not in {"HM", "SC", "PZ", "PO", "CM", "CGU", None}:
        print("Invalid campus provided, use \"HM\", \"CM\", \"SC\", \"PZ\", \"PO\" or \"CGU\"")
        exit(0)
    # target should be in the format "CSCI140"
    search_result = get_portal_html(browser, target, campus)
    desc = find_desc_from_portal_html(search_result, target, browser)
    print(desc + "\n")
