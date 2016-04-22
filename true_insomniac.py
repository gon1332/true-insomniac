#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

LOGIN_URL = "http://www.insomnia.gr/index.php?app=core&module=global&section=login"
TARGET_URL = "http://www.insomnia.gr/index.php?app=core&module=search&do=user_activity&mid=223995"
USER = "username"
PASS = "password"

driver = webdriver.PhantomJS()
driver.get(LOGIN_URL)
assert "Insomnia" in driver.title

try:
    user_elem = driver.find_element_by_name("ips_username")
    pass_elem = driver.find_element_by_name("ips_password")
except NoSuchElementException as e:
    print(e)
    driver.close()
    exit()

user_elem.send_keys(USER)
pass_elem.send_keys(PASS)

try:
    pass_elem.submit()
except NoSuchElementException as e:
    print(e)
    driver.close()
    exit()

driver.get(TARGET_URL)

try:
    unread_elems = driver.find_elements_by_class_name("unread")
except NoSuchElementException as e:
    print(e)
    driver.close()
    exit()

print("\u2605", len(unread_elems))

driver.close()
