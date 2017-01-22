import time
import os
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import autoit
import shutil
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
PLUGINS = 'always-authorize-plugins'

project_suffix = "Project1"
save_dir = 'C:/Users/username/Desktop/'+project_suffix

if os.path.exists(save_dir):
    shutil.rmtree(save_dir)
os.makedirs(save_dir)

chromedriver = "C:/PythonScripts/chromedriver.exe"

options = Options()
options.add_argument('--%s=false' % PLUGINS)
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)


driver.get('http://server/jira/secure/Dashboard.jspa');

time.sleep(1) # Let the user actually see something!
login = driver.find_element_by_name('os_username')
login.send_keys('username')
pw = driver.find_element_by_name('os_password')
pw.send_keys('password')
submit_button = driver.find_element_by_id('login')
submit_button.submit()
time.sleep(1) # Let the user actually see something!

def check_exists_by_id(text):
    try:
        driver.find_element_by_id(text)
        print('found'+text)
    except NoSuchElementException:
        print('not found' + text)
        return False
    return True

for number in range(0, 100000):
    issuenum =  project_suffix +'-'+str(number)
    url = 'http://server/jira/browse/'+issuenum
    driver.get(url);
    time.sleep(1)
    if(check_exists_by_id('issue_key_'+project_suffix+'-'+str(number))):
        time.sleep(1)
        if(driver.find_elements_by_xpath("//*[contains(text(), 'File Attachments:')]")):
            print('found file attachments')
            time.sleep(1)
            driver.find_element_by_xpath("//*[contains(text(), 'File Attachments:')]").click()
            row_count = len(driver.find_elements_by_xpath("//*[@id='issueContent']/p[3]/table/tbody/tr/td/table/tbody/tr"))
            current_url = driver.current_url
            for number in range(2, row_count+1):
                driver.get(current_url)
                actionChains = ActionChains(driver)
                image_iteration = "//*[@id='issueContent']/p[3]/table/tbody/tr/td/table/tbody/tr["+str(number)+"]/td[3]/a"
                time.sleep(1)
                url = driver.find_element_by_xpath("//*[@id='issueContent']/p[3]/table/tbody/tr/td/table/tbody/tr[" + str(number) + "]/td[3]/a").get_attribute('href')
                #if "mp4" not in url:
                #driver.find_element_by_xpath("//*[@id='issueContent']/p[3]/table/tbody/tr/td/table/tbody/tr["+str(number)+"]/td[3]/a").click()
                attachment = driver.find_element_by_xpath("//*[@id='issueContent']/p[3]/table/tbody/tr/td/table/tbody/tr["+str(number)+"]/td[3]/a")
                time.sleep(1)
                actionChains.context_click(attachment).perform()
                time.sleep(1)
                action = webdriver.common.action_chains.ActionChains(driver)
                action.move_to_element_with_offset(attachment, 30000,30000)
                time.sleep(1)
                autoit.send("{down}{space}{down}{down}{down}{enter}")
                time.sleep(3)
                autoit.send("{enter}")
                filename = url.rsplit('/', 1)[-1]
                time.sleep(1)
                current_location = "C:/Users/username/Downloads/"+filename
                save_location = save_dir + "/" + issuenum
                if not os.path.exists(save_location):
                    os.makedirs(save_location)
                save_location_file = save_location + "/" + filename
                timecounter = 0
                while not os.path.exists(current_location):
                    time.sleep(3)
                    timecounter =+1
                    if (timecounter > 20):
                        break
                if os.path.isfile(current_location):
                    shutil.move(current_location, save_location_file)
                else:
                    raise ValueError("%s isn't a file!" % current_location)
                time.sleep(1)

