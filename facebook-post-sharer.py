from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Disable notifications when Facebook asks to show notifications
options = Options()
options.add_argument("--disable-notifications")

# Initiate the browser
driver  = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

# Open the Website
driver.get('https://www.facebook.com/')
print("Logging in...")


# Your Facebook credentials
fb_name = "wrong credentials"
fb_pass = ""

print("Wrong credentials. Edit the code.")
exit()

# Fill credentials
driver.find_element_by_name("email").send_keys(fb_name)
driver.find_element_by_name("pass").send_keys(fb_pass)
# Click Log In
driver.find_element_by_name('login').click();

print("Loading post...5 sec...")
sleep(5)
# Go to page
#driver.get('https://www.facebook.com/ISACC.org')
driver.get('https://www.facebook.com/ISACC.org/photos/a.413075825329/10159332647675330/')

# Loading post...
print("Loading post...3 sec...")
sleep(3)

# Click choose how to interact
print("Clicking choose how to interact...")
driver.find_element_by_xpath("//button[@aria-label='Voice Selector']").click()

# Interact as user
print("Selecting how to interact...3 sec...")
sleep(3)
# Select how to interact
actions = ActionChains(driver) 
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.ENTER)
actions.perform()
print("Loading user account interact...3 sec...")
sleep(3)

# Click Share button
#print("Clicking Share button...")
driver.find_element_by_xpath("//div[@aria-label='Send this to friends or post it on your Timeline.']").click()

# Load sharing options
print("Loading sharing options...1 sec...")
sleep(1)
# Press share in Messenger
n = 3
actions = ActionChains(driver) 
actions.send_keys(Keys.TAB * n)
actions.send_keys(Keys.ENTER)
actions.perform()

# Load Sending options
print("Loading Send in Messenger options...5 sec...")
sleep(5)


print("Clicking send in 5 sec...")
sleep(5)
# Click Send
driver.find_element_by_xpath("//span[text() = 'Send']").click()
element = driver.find_element_by_xpath("//span[text() = 'Send']").click()

# Do this 3453 (MPM friends count) times plus 20 (recent and groups buffer)
for i in range(3473):
    print("Sent: " + i)
    print("Page reloading...")
    sleep(5) # it will load slowly in a while
    driver.find_element_by_xpath("//span[text() = 'Send']").click()


print("Exiting in 10 sec...") # ---------------------------------
exit()
