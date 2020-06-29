####### Do Imports #######
from selenium import webdriver
from time import sleep
import sys

####### Initialize variables & constants #######
CHROMEDRIVER_PATH = "C:\\webdriver\\chromedriver.exe"

BELL_HOMEPAGE = "https://www.bell.ca/Mobility/Smartphones_and_mobile_internet_devices"

VALID_DRIVER_MSG = "Please select a valid webdriver to run this application. Default is: chrome"
INPUT_MSG = "Please select the device number for pricing details: "

DEVICE_ITEM_XPATH = "//*[@id='div_product_list_item_div_product_list_item_{}']/div/div[3]"
LINK_TO_DEVICE = "/html/body/main/div[5]/div/div[3]/div[{}]/div/a"
PLAN_DETAILS = "//*[@id='bcx-order-now-group-smartpay']/div[1]"
DEVICE_DETAILS = "//*[@id='productPriceDiv']/div[1]/div/div/div[2]/div[1]/h1"


####### Initialize webdriver #######
def init_driver(browser="chrome"):
    if (browser != "chrome"):
        raise Exception(VALID_DRIVER_MSG)
    else:
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
        return driver


####### Welcome Message #######
def welcome_user(name="Karanbir Singh"):
    print("Welcome, {} !! Please find the list of top 12 devices below:".format(name))


####### Get Bell's Home Page and get list of devices #######
def get_page(driver, page):
    driver.get(page)


####### Util methods #######
def maximize_window(driver):
    driver.maximize_window()


def wait_implicitly(driver, time=1000):
    driver.implicitly_wait(time)


def print_chars(char="-", times=1):
    print(char * times)


####### Print options to select from and wait for user input #######
def show_device_list(driver):
    get_page(driver, BELL_HOMEPAGE)
    wait_implicitly(driver, 100)

    device_dict = {}
    device_name = {}

    for i in range(0, 12):
        var = DEVICE_ITEM_XPATH.format(str(i))
        device = driver.find_element_by_xpath(var)
        n = str(i + 1)
        device_name[n] = str(device.text)

        element = n + ". " + device_name[n]
        device_dict[n] = driver.find_elements_by_xpath(LINK_TO_DEVICE.format(n))
        print(element)

    device_no = str(
        input("\nPlease select the device number b/w 1-12 for pricing details or any other character to quit: "))

    while (int(device_no) > 0 and int(device_no) < 13):
        get_device_details(driver, device_dict, device_no, device_name[device_no])
        driver.back()
        sleep(3)
        show_device_list(driver)

    shutdown_application(driver)


####### Get plan details of selected device #######
def get_device_details(driver, device_dict, id, device_name):
    device_dict[id][0].click()

    details = driver.find_elements_by_xpath(PLAN_DETAILS)
    wait_implicitly(driver, time=100)

    print_chars("\n", 2)
    print_chars("*", 50)
    print("You have selected {}".format(device_name))
    print_chars("*", 50)

    print("The Plan Details are: \n")

    for i in details:
        print(i.get_attribute("innerText"))

    print("\n\n")


####### Exit driver #######
def shutdown_application(driver):
    driver.quit()
    sys.exit(0)


if __name__ == "__main__":
    try:
        driver = init_driver(browser="chrome")
        welcome_user(name="Karanbir")
        get_page(driver, BELL_HOMEPAGE)
        wait_implicitly(driver, time=100)
        show_device_list(driver)
        sleep(20)
    except Exception as e:
        raise e
    finally:
        shutdown_application(driver)
