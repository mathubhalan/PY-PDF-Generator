# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 16:10:45 2017

@author: Mathu_Gopalan
"""
#Read URL
# get shots path
# gen PDF
# option to execute conditions
import os, yaml, time
from selenium import webdriver
from urllib.parse import urlparse
from PIL import Image
import util
import imutils

def readConfig(confg):
    global BaseFolder, InputFile,SnapFolder,login_form,credentials
    global form_login,form_pass,form_submit
    with open(confg,'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        #print (cfg)
    for section in cfg:
        BaseFolder = cfg["Path"]["BaseFolder"]
        InputFile = cfg["Path"]["InputFile"]
        SnapFolder = cfg["Path"]["SnapFolder"]
        login_form = cfg["Login"]["LoginPath"]
        credentials = cfg["Login"]["Credentials"]        
        form_login = cfg["Login"]["form_user_name"]
        form_pass = cfg["Login"]["form_user_pass"]
        form_submit = cfg["Login"]["form_user_submit"]        
    print("Config completed")
    create_basefolder(BaseFolder,SnapFolder,InputFile)

def create_basefolder(BaseFolder,SnapFolder,InputFile):
    print ("creating folders basefolder : {}, snap folder{}..".format(BaseFolder,SnapFolder))
    if not os.path.exists(BaseFolder):
        os.makedirs(BaseFolder)
    #create snap folder    
    if not os.path.exists(SnapFolder):
        os.makedirs(SnapFolder)          
    print("folder creation completed")
    
def takeSnap():
    remdr = webdriver.Chrome()
    remdr.maximize_window()        
    remdr.get(login_form)
    remdr.implicitly_wait(2000)
    time.sleep(2)
    remdr.find_element_by_id(form_login).send_keys(credentials.split("/")[0])
    remdr.find_element_by_id(form_pass).send_keys(credentials.split("/")[1])
    remdr.find_element_by_xpath(form_submit).click()
    remdr.implicitly_wait(200)  
    time.sleep(2)
    with open(InputFile) as csvfile:
        for url in csvfile:
            remdr.get(url.strip())
            print("Snapping {}".format(url))
            time.sleep(3)
            key = remdr.title
            key=key.replace(" ","").strip()
            key=key.replace("|","_")
            if len(key)>240:
                key = key[0:239]
            remdr.implicitly_wait(5000)
            print(key)
            util.fullpage_screenshot(remdr,SnapFolder,key)

def main():
    readConfig("config.yml")
    takeSnap()

if __name__ == "__main__":
    main()

    
