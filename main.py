from selenium import webdriver
import time
import argparse


def bounce(driver):
    driver.find_element_by_xpath('*//div[@class="content-wrapper active"]/img').click()
    time.sleep(3)
    try:
        driver.find_element_by_xpath('//input[@name="checker"]').click()
    except Exception:
        driver.find_element_by_xpath('//*[@id="sLightbox_container"]/div/div[1]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//input[@name="checker"]').click()
    time.sleep(3)
    #The bounce button is inside an iFrame, lets switch to the iFrame
    iframe = driver.find_element_by_xpath('//*[@id="feed"]/tbody/tr[3]/td/iframe')
    driver.switch_to.frame(iframe)
    print(f'switch frame to {driver.current_window_handle}')
    # # driver.find_element_by_id('//div[@class="table_Details"]')
    driver.find_element_by_xpath('//*[@id="bounceRatingOrderBtn"]/span').click()
    time.sleep(4)
    print("Post Bounced Successfuly")


def login(driver, arguments):
    try:
        driver.find_element_by_xpath('*//input[@id="userName"]').send_keys(arguments.email)
        driver.find_element_by_xpath('*//input[@id="password"]').send_keys(arguments.password)
        driver.find_element_by_xpath('*//input[@id="submitLogonForm"]').click()
        if driver.current_url == 'https://my.yad2.co.il/newOrder/index.php?action=connect':
            raise Exception
        return True
    except Exception:
        print('Email or password are wrong. unable to log-in, closing')
        driver.quit()
        return False

def get_arguments():
    parser = argparse.ArgumentParser(description='"python main.py your-email your-password')
    parser.add_argument('email', help='Valid email of user in Yad2')
    parser.add_argument('password', help='Valid password of user in Yad2')
    return parser.parse_args()


def main():
    args = get_arguments()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("headless")
    browser = webdriver.Chrome('./chromedriver.exe', options=chrome_options)
    browser.get('https://my.yad2.co.il/login.php')
    if not login(browser, args):
        print('Could not log-in, check your credentials.')
        return 1
    bounce(browser)
    time.sleep(2)
    browser.quit()


if __name__ == '__main__':
    main()
