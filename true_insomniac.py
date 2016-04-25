#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

LOGIN_URL = "http://www.insomnia.gr/index.php?app=core&module=global&section=login"
TARGET_URL = "http://www.insomnia.gr/index.php?app=core&module=search&do=user_activity&mid=223995"
USER = "username"
PASS = "password"

# create driver
driver = webdriver.PhantomJS()
atexit.register(driver.close)

# login
driver.get(LOGIN_URL)
driver.find_element_by_id("ips_username").send_keys(USER)
driver.find_element_by_id("ips_password").send_keys(PASS)
driver.find_element_by_class_name("input_submit").submit()

# get unread messages
driver.get(TARGET_URL)
unread_elems = driver.find_elements_by_class_name("unread")
print("\u2605", len(unread_elems))
