''' IMPORTS'''
import os
import sys
import math
import time
import datetime
import traceback
import re # RegEx
import logging
try:
    if not os.path.exists('log'):
        os.makedirs('log')
    logging.basicConfig(filename='./log/smai.log', encoding='utf-8', level=logging.DEBUG,
        format='%(asctime)s - %(name)s (line: %(lineno)d) - %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')
except:
    traceback.print_exc()
    
finally:
    if not os.path.exists('resources'):
        os.makedirs('resources')

from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import SessionNotCreatedException


''' CONSTANTS '''
CURRENT_PATH = os.path.abspath(".")
configuration_file_directory = CURRENT_PATH + "/resources/" + "settings.txt"


''' VARIABLES '''
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
config = ConfigParser()
config.read(configuration_file_directory)


''' FUNCTIONS '''

def delay(sec):
    if not math.isnan(sec):
        # print("Delay for {} sec, ".format(sec), end="")
        print("Delay for {} sec... ".format(sec))
        # for countdown in reversed(range(sec)):
            # print("{}...".format(countdown), end="", flush=True)
            # time.sleep(1)
        # print()

        start = time.time()
        end = time.time()

        while end - start < sec:
            # print(end - start)
            # print(".", end="", flush=True)
            end = time.time()

        # print("hello")
        # end = time.time()
        # print(end - start)
    else:
        raise Exception("Parameter sec is not a Number.");


waiting_per_action = int(config['DEFAULT']['waiting time per action'])

post_actions_file_dir = config['DEFAULT']['actions']


# Using readlines()
post_actions_file = open(post_actions_file_dir, 'r')
post_actions_list_untrimmed = post_actions_file.readlines()
post_actions_file.close()
post_actions_list = []
for action_line in post_actions_list_untrimmed:
    post_actions_list.append(action_line.strip())

def clickByXPath(xpath):
    delay(waiting_per_action)

    logger.info("Click by xpath: " + xpath)
    try:
        element = browser.find_element_by_xpath(xpath)
        if(element != None):
            element.click()
            return True
        else:
            logger.warning("Element is none...")
            # delay(1)
    except NoSuchElementException:
        # print("No name search field found...", end="", flush=True)
        #logger.warning("No more posts to unfollow...")
        #sys.exit()
        # Try to try again but scroll down first.
        # time.sleep(1)
        # Google "facebook keyboard shortcuts next post"
        #logger.info("remove: trying to find element");
        #element = browser.find_element_by_xpath(xpath)
        #browser.execute_script("arguments[0].scrollIntoView();",element)
        #time.sleep(20)
        
        # Try the alternative. Try again.
        #logger.warning("Post Action Menu not found on the page...")
        logger.warning("Post Action Menu Option not found...")
        
    except NoSuchWindowException:
        logger.warning("Browser window closed unexpectedly...")
    except WebDriverException:
        logger.warning("Browser window unreachable...")
    except:
        logger.exception("Something went wrong...")

    return False
# End clickByXPath()


''' START '''

repeat_unfollow_count = int(config['DEFAULT']['repeat'])

logger.info("==============================================================================")
logger.info("Facebook Unfollower")
logger.info("Program running...")


# Evaluate URL
url = config['DEFAULT']['link']

browser = None

options = webdriver.ChromeOptions()
# Disable notifications when Facebook asks to show notifications
options.add_argument("--disable-notifications")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver_path = CURRENT_PATH + "/" + config['DEFAULT']['driver'] # "/chromedriver_win32/chromedriver.exe"
driver_relative_path_name = config['DEFAULT']['driver']
try:
    logger.info("Instanciating driver...")
    logger.info("from " + driver_path)
    browser = webdriver.Chrome(driver_path, options=options)
   
    print("Opening browser...")
    browser.get(url)
    print("Browser opened...")

    # Wait until successfully logged in
    logger.info("Waiting to login...")
    login_success = False
    login_timeout = int(config['DEFAULT']['inactivity_timeout'])

    print("Waiting to login for {} sec: ".format(login_timeout), end="\n")
    for countdown in reversed(range(login_timeout)):
        try:
            # print("try...")
            # print("{}...".format(countdown), end="", flush=True)
            
            # login_reference_element_xpath = "//a[@aria-label='Facebook']" # Sometimes present even though not logged in
            # login_reference_element_xpath = "//button[@aria-label='Voice Selector']" 
            login_reference_element_xpath = "//a[@aria-label='Home']"
            home = browser.find_element_by_xpath(login_reference_element_xpath)
            # print("home")
            # print(home)
            if(home != None):
            # if (browser.find_element_by_xpath(login_reference_element_xpath)):
                login_success = True
                break
            else:
                # print("else...")
                print("{}          ".format(countdown), end="\r", flush=True)
        except NoSuchElementException:
            print("{}                ".format(countdown), end="\r", flush=True)
            # traceback.print_exc()
            time.sleep(1)
        except NoSuchWindowException:
            logger.warning("Browser window closed unexpectedly...")
            # traceback.print_exc()
            break
        except WebDriverException:
            logger.warning("Browser window unreachable...")
            logger.warning(traceback.print_exc())
            break
        except:
            logger.exception("Something went wrong during login...")
            # traceback.print_exc()
            break

        if countdown == 0:
            logger.info("Login timeout...")
            print()
    # End - for countdown in reversed(range(login_timeout))

    if login_success:
        logger.info("\nLogin success...")

        begin_unfollow = True
        if begin_unfollow:
            logger.info("\nClear any Facebook popups...")
            delay(5)
        
            logger.info("Initiating automation...")
            
            # For finding Post Action Menu
            scroll_height = 500
            scroll_increment = 300
            
            print(post_actions_list)
            
            for index in range(repeat_unfollow_count):
                logger.info("Retrying... [{}/{}]".format(index+1, repeat_unfollow_count))

                if clickByXPath("//div[@aria-label='Actions for this post']"): # Action menu
                    if clickByXPath("//a[@aria-label='hide post']"): # X button because no option in action menu
                        continue
                    if clickByXPath("//span[text()='Close']"):
                        browser.refresh()
                        continue
                    for action_line in post_actions_list:
                        action_list = action_line.split(" > ")
                        for action in action_list:
                            clickByXPath("//span[contains(text(),'{}')]".format(action))
                        continue
                
                    #if clickByXPath("//span[contains(text(),'Unfollow ')]"): # Unfollow
                    #    continue
                    #if clickByXPath("//span[text()='Hide ad']"): # Hide ad
                    #    clickByXPath("//span[text()='Irrelevant']")
                    #    clickByXPath("//span[text()='Done']")
                    #    continue
                    #if clickByXPath("//span[text()='Hide post']"): # Hide post
                    #    continue
                    #if clickByXPath("//a[@aria-label='hide post']"): # X button because no option in action menu
                    #    continue
                    #if clickByXPath("//span[text()='Hide People You May Know']"):
                    #    continue
                    #if clickByXPath("//span[text()='Reload page']"):
                    #    continue
                    #if clickByXPath("//span[text()='Close']"):
                    #    browser.refresh()
                    #    continue
                else:
                    logger.info("Scrolling down to find the Post Action Menu")
                    #element = browser.find_element_by_xpath("//div[@aria-label='Actions for this post']")
                    #browser.execute_script("arguments[0].scrollIntoView();", element)
                    jump_size = str(scroll_height ++ scroll_increment)
                    #browser.execute_script("window.scrollBy(0,{})".format(jump_size),"")
        else:
            logger.warning("Aborting automation...")
    else:
        logger.warning("\nLogin failed...")
        # close_driver(browser)
        if browser != None:
            try:
                browser.close()
                logger.info("Driver closed...")
            except:
                #logger.warning("chromedriver.exe is already closed.")
                logger.warning(driver_relative_path_name + " is already closed.")
# End try - if driver is properly instanciated
except SessionNotCreatedException:
    #traceback.print_exc()
    logger.error("Incompatible Driver Error.")

except FileNotFoundError:
    logger.warning(driver_relative_path_name + " is not found.")
    
except:
    #logger.error("chromedriver.exe is not in found.")
    #logger.warning(driver_path + " is not found.")
    # delay(10)
    # traceback.print_exc()
    logger.exception('Got exception on main handler')
    #raise

finally:
    if browser == None:
        logger.info("Check your browser version, update driver location in settings.txt, tested only for Chrome.")
        logger.info("Get the updated Selenium Driver here:")
        logger.info("https://chromedriver.chromium.org/downloads/")
        logger.info("Also see")
        logger.info("https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/")

        

if browser != None:
    try:
        browser.close()
        logger.info("Browser closed...")
    except:
        #logger.warning("chromedriver.exe is already closed.")
        logger.warning(driver_relative_path_name + " is already closed.")

logger.info("Program terminated...")
input("Close the window to exit...")

