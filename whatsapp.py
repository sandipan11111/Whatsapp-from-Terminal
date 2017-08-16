from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from threading import Thread

import sched
import time
import sys
import optparse

incoming_scheduler = sched.scheduler(time.time, time.sleep)
lastprinted = 0

msglist=[]
def openchat(driver,name):
    search=driver.find_element(By.XPATH,'//*[@id="side"]//input')
    search.clear()
    search.click()
    search.send_keys(name)
    search.send_keys(Keys.RETURN)


def send(driver,msg):
    inp=driver.find_element(By.XPATH,'//*[@id="main"]//footer//div[@class="input"]')
    inp.click()

    typ=ActionChains(driver)
    typ.send_keys(msg)
    typ.send_keys(Keys.RETURN)
    typ.perform()

def receive(driver):

    incoming_scheduler.enter(5,1,helper,(driver,incoming_scheduler))
    incoming_scheduler.run()




def helper(driver,scheduler):
    global lastprinted

    msgs=driver.find_elements(By.XPATH,'//*[@id="main"]//div[contains(@class,"message-text")]')

    """"
    while True:
    if len(msglist) > 0:
        tostop=msglist[-1]
        flag=False
        for msg in msgs:
            if flag==True:
                print (msg.text)
                msglist.append(msg.text)
            if msg.text == tostop:
                flag=True
    """

    try:
        last_msg=msgs[-1]
        last=last_msg.get_attribute('data-id')
    except IndexError:
        last=None
    if last:
        #for incoming msgs
        if last[:5] == 'false':
            if last==lastprinted:
                pass
            else :
                index=len(msgs)

                for i,msg in reversed(list(enumerate(msgs))):

                    curr=msg.get_attribute('data-id')
                    if curr[:4] == 'true' or curr==lastprinted:
                        index=i
                        break

                for i in range(index+1,len(msgs)):
                    lastprinted=msgs[i].get_attribute('data-id')
                    print(msgs[i].text)



    incoming_scheduler.enter(5,1,helper,(driver,scheduler,))



parser=optparse.OptionParser()
parser.add_option('-n','--name',dest='name',help='Your Name')

(options,args)=parser.parse_args()

driver=webdriver.Chrome()
driver.get("https://web.whatsapp.com")

if options.name is None:
    options.name=input("Enter:")

while True:
    check=input("Is Connected(y/n)")
    if(check.lower()=='y'):
        break


openchat(driver,options.name)
thread1=Thread(target=receive,args=(driver,))
thread1.start()
#helper(driver)

print("Send Messages to" + options.name )

while True:
    msg=input()
    send(driver,msg)
    msglist.append(msg)
