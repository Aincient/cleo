import json
import os
import signal
import subprocess
import uuid

from selenium import webdriver
from bs4 import BeautifulSoup

__all__ = (
    'phantom_js_clean_up',
    'phantom_js_get',
)


def phantom_js_clean_up():
    """Clean up Phantom JS.

    Kills all phantomjs instances, disregard of their origin.
    """
    processes = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = processes.communicate()

    for line in out.splitlines():
        if b'phantomjs' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)


def phantom_js_get(url, raw=False):
    """Get.

    :param url:
    :return:
    """
    # Open a PhantomJS
    driver = webdriver.PhantomJS()
    # Get URL
    driver.get(url)
    # Extract the raw HTML
    html_source = driver.page_source
    # Exit PhantomJS
    driver.quit()
    # Make sure PhantomJS is unloaded from memory
    phantom_js_clean_up()

    if raw:
        return html_source

    # Get clean JSON
    soup = BeautifulSoup(html_source, "lxml")
    json_source = soup.get_text()

    # Convert to dict
    try:
        dict_data = json.loads(json_source)
    except (TypeError, json.JSONDecodeError):
        return {}
    return dict_data


def phantom_js_download_image(url, destination_directory):
    """Get.

    :param url:
    :param destination_directory:
    :return:
    """
    # Open a PhantomJS
    driver = webdriver.PhantomJS()
    # Get URL
    driver.get(url)
    img_val = driver.get_screenshot_as_png()
    print(img_val)
    # Extract the raw HTML
    filename = os.path.join(
        destination_directory,
        "{}.{}".format(str(uuid.uuid4()), 'jpg')
    )
    driver.save_screenshot(filename)
    # Exit PhantomJS
    driver.quit()
    # Make sure PhantomJS is unloaded from memory
    phantom_js_clean_up()

    return filename
