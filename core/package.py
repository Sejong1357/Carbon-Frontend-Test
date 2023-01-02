# -*- coding: utf-8 -*-

# system info
import platform

# 외부 실행 제어 모듈
import os
import subprocess
import io
import re

try:
    import cv2															# pip install opencv-python
except:
    subprocess.call("pip install opencv-python ", shell=True, timeout=1000)

import sys
import json
import time
import numpy 														# pip install numpy
import base64 														# pip install pybase64
import random
from random import randrange
import logging
import requests
import datetime
from datetime import datetime, timedelta
import shutil
import re
import keyboard


try:
    import psutil
except:
    subprocess.call("pip install psutil", shell=True, timeout=1000)

try:
    import pydirectinput
except:
    subprocess.call("pip install pydirectinput", shell=True, timeout=1000)

import unittest
from datetime import datetime



import signal
try:
    from PIL import Image, ImageFilter
except:
    subprocess.call("pip install pillow", shell=True, timeout=1000)

try:
    import pyautogui
except:
    subprocess.call("pip install pyautogui", shell=True, timeout=1000)





# SELENIUM WEBDRIVER 제어 모듈 										# pip install selenium
try:
    from selenium import webdriver
except :
    subprocess.call("pip install selenium", shell=True, timeout=1000)
from selenium.webdriver.remote.command import Command

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.alert import Alert

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import *

# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.options import Options
from selenium.webdriver.ie.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# Chrome driver 제어 모듈                                       # pip install chromedriver_autoinstaller
try:
    import chromedriver_autoinstaller #크롬 업데이트
except:
    subprocess.call("pip install chromedriver_autoinstaller", shell=True, timeout=1000)

try:
    from webdriver_manager.chrome import ChromeDriverManager
except:
    subprocess.call("pip install webdriver-manager", shell=True, timeout=1000)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
