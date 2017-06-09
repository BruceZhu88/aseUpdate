# -*- coding: utf-8 -*-
'''
Created on 2016.10

@author: bruce.zhu
'''

import datetime
import requests
from utility.createHTMLReport import *
from utility.logger import Logger
from utility.config import getconfig
from selenium import webdriver


#parent_path = os.path.realpath(os.path.join(os.getcwd(), ".."))
local_version1,local_version2,old_version,new_version,IP,cycle,title=getconfig.getparameters('./config.ini')
#driver = webdriver.Chrome("%s\chromedriver2.9.exe"%os.getcwd())
driver = webdriver.Firefox()
driver.get(IP) #open setting page

#s = unicode ("成 ", "utf-8")

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def screenshot(info):
    logging.log(logging.INFO, "%s\%s_%s.jpg"%(shot_path,info,time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) ))
    driver.get_screenshot_as_file("%s/%s_%s.jpg"%(shot_path,info,time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) ))
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def check_connect(url):
    try:
        r = requests.get(url, allow_redirects = False)
        status = r.status_code
        if status == 200:
            logging.log(logging.INFO, 'Network is ok')
            return True
        else:
            screenshot("Network error")
            logging.log(logging.ERROR, 'Network error!!!!')
            return False
    except:
        screenshot("Network error")
        logging.log(logging.ERROR, 'Network error!!!!')
        return False

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#make screen shot directory
def make_shot_dir():
    #shot_conf = dict(root_run = os.getcwd())
    run_shot_dir = os.path.realpath(os.path.join(os.getcwd(), "..", 'Shot'))

    if not os.path.exists(run_shot_dir):
        os.makedirs(run_shot_dir)

    return run_shot_dir
    #shot_conf['runshot_dir'] = run_shot_dir
    #return shot_conf

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def find_element(element):
    repeat = 10
    i = 0
    for i in range(1,repeat+1):
        try:
            driver.find_element_by_xpath(element)
            break
        except:
            logging.log(logging.INFO, "Try to find %s  ----%s times!"%(element,i))
            time.sleep(1)

    if i==repeat:
        logging.log(logging.INFO, "Can not find relevant element [%s]! Please check your network!"%element)
        logging.log(logging.INFO, "Please restart test!.............")
		screenshot("Cannot_find_element")
        sys.exit()
        return

    return driver.find_element_by_xpath(element)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def update_percentage():
    time.sleep(10)
    """
    f=0
    while f==0:
        time.sleep(2)
        if check_popup():

            driver.switch_to_frame("rightFrame")
            try:
                str_per=find_element("//*[@id='DownloadProgressMsg']").text #Firmware upload status: 42% completed.
                print "english"
            except:
                time.sleep(0.5)
            '''
            try:
                str_per=find_element("//*[@id='ProgressMsg']").text #固件上传状态：完成 XX%   //*[@id="ProgressMsg"]
                print "chinese"
            except:
                time.sleep(0.5)
            '''
            print str_per
            if "Firmware" in str_per:
				a,b = str_per.split(": ")
				c,d = b.split("%")
				per = c
            else: #<div id="ProgressMsg" class="Bo-text">固件上传状态：完成 50%。</div>
				a,b = str_per.split(s)
				c,d = b.split("%")
				per = c
            if int(per)>85: #variable per must turn to integer
                f=1
                print per
                time.sleep(15)
        else:
            return False
    """
    f=0
    while f==0:
        time.sleep(8)
        if check_popup()==False:
            driver.switch_to_default_content()
            driver.switch_to_frame("rightFrame")
            try:
                #print find_element("//*[@id='ConfirmUpdateDone']").text
                ConfirmUpdateDone = find_element("//*[@id='ConfirmUpdateDone']")
                ConfirmUpdateDone.click()
                f=1
                return True
            except:
                f=0
        else:
            return False
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def check_version(v):
    driver.switch_to_default_content()
    driver.switch_to_frame("rightFrame")
    softwareVersion = find_element("//*[@id='softwareVersion']")
    version = softwareVersion.text
    logging.log(logging.INFO, "DUT current version is %s"%version)
    if v==version:
        #success_time=success_time+1
        logging.log(logging.INFO, "Update success!")
        return True
    else:
        logging.log(logging.INFO, "Update fail!")
        return False

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def check_popup():
    global Network_Error
    driver.switch_to_default_content()
    try:
        driver.find_element_by_class_name("imgButtonYes").is_displayed()

        screenshot("%s_popup"%Network_Error)
        driver.find_element_by_class_name("imgButtonYes").click()
        logging.log(logging.INFO, "Network unavailable")
        Network_Error+=1
        return True
    except:
        return False



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def update_local(local_file,version):
    driver.switch_to_frame("rightFrame")

    LocalUpdateButton = find_element("//*[@id='LocalUpdateButton']")
    LocalUpdateButton.click()

    datafile = find_element("//*[@id='datafile']")
    datafile.send_keys('%s'%local_file)

    time.sleep(1)
    LoadFileButton = find_element("//*[@id='LoadFileButton']")
    LoadFileButton.click()

    logging.log(logging.INFO, "Uploading %s file..."%local_file)
    f=0 #If uploading success, f=1, end while
    while f==0:
        time.sleep(5)
        if check_popup()==False:
            driver.switch_to_frame("rightFrame")
            NewSWVersion = find_element("//*[@id='NewSWVersion']")
            version_name = NewSWVersion.text

            print('*', end = '')
            if version_name != "":
                print(version_name)
                if version_name==version:
                    logging.log(logging.INFO, "Uploading success!")
                    time.sleep(10)

                    LocalUpdateConfirmYes = find_element("//*[@id='LocalUpdateConfirmYes']")
                    LocalUpdateConfirmYes.click()

                    logging.log(logging.INFO, "Start burn into...!")
                    f=1
                else:
                    logging.log(logging.INFO, "Version %s does not matchold_version %s, please check your config.ini!"%(version_name,old_version))
        else:
            return False
    if update_percentage()==False:
        return False

    return True
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def update_full():
    global downgrade_time,update_time
    logging.log(logging.INFO, IP)
    logging.log(logging.INFO, driver.title)

    time.sleep(2)
    driver.switch_to_default_content()
    driver.switch_to_frame("rightFrame")

    softwareVersion = find_element("//*[@id='softwareVersion']")
    current_version = softwareVersion.text

    logging.log(logging.INFO, "DUT current version is %s"%current_version)
    ## Switch back to main window
    driver.switch_to_default_content()

    time.sleep(2)
    driver.switch_to_frame("leftFrame")
    SwUpdatePage = find_element("//*[@id='SwUpdatePage']/span")
    SwUpdatePage.click()

    driver.switch_to_default_content()

    if (current_version!=old_version) and (current_version!=new_version):
        update_local(local_version2, new_version)
        time.sleep(15)
        check_version(new_version)
        return

    if local_version1 == local_version2:
        local_file = local_version1
        if current_version==new_version:
            logging.log(logging.INFO, "Downgrade on local")

            update_local(local_file, old_version)
            time.sleep(15)
            if check_version(old_version):
                logging.log(logging.INFO, "Downgrade success from %s to version %s on local"%(new_version,old_version))
                downgrade_time+=1

        else:
            logging.log(logging.INFO, "Update on server")
            time.sleep(2)
            driver.switch_to_frame("rightFrame")

            f=0 #If uploading success, f=1, end while
            while f==0:
                if check_popup()==False:
                    driver.switch_to_frame("rightFrame")
                    NewSWVersion = find_element("//*[@id='NewSWVersion']")
                    check_nv = NewSWVersion.text #check new version
                    if check_nv==new_version:
                        UpdateFromNetworkButton = find_element("//*[@id='UpdateFromNetworkButton']")
                        UpdateFromNetworkButton.click()
                        time.sleep(3)
                        NetworkUpdateConfirmYes = find_element("//*[@id='NetworkUpdateConfirmYes']")
                        NetworkUpdateConfirmYes.click()
                        logging.log(logging.INFO, "Start update!")
                        f=1
                else:
                    return False
            if update_percentage()==False:
                return False
            time.sleep(15)
            if check_version(new_version):
                logging.log(logging.INFO, "Update success from %s to version %s on internet"%(old_version,new_version))
                update_time+=1
    #**************************************************************************************************************
    else:
        if current_version==new_version:
            local_file = local_version1
            versionCheck = old_version
            logging.log(logging.INFO, "Downgrade to version %s just with local file"%versionCheck)
        else:
            local_file = local_version2
            versionCheck = new_version
            logging.log(logging.INFO, "Update to version %s just with local file"%versionCheck)

        update_local(local_file, versionCheck)
        time.sleep(15)
        if check_version(versionCheck):
            if versionCheck==old_version:
                logging.log(logging.INFO, "Downgrade success from %s to version %s on local"%(new_version,old_version))
                downgrade_time+=1
            elif versionCheck==new_version:
                logging.log(logging.INFO, "Update success from %s to version %s on internet"%(old_version,new_version))
                update_time+=1
            else:
                logging.log(logging.ERROR, "No such version! Error")

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Main()
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__=='__main__':
    update_time=0
    downgrade_time=0
    Network_Error=0
    Run_status="Running"
    update="Update success from %s to version %s on internet"%(old_version,new_version)
    downgrade="Downgrade success from %s to version %s on local"%(new_version,old_version)
    shot_path=make_shot_dir()

    start_time=time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    log_conf = Logger.init_logger('project.log')
    start=time.time()

    i=1
    for i in range(1,int(cycle)+1):
        logging.log(logging.INFO, "This is %i times----------------------------------------"%i)
        if check_connect(IP+"/index.fcgi"):
            #when version file have been download from server(on updating),but the net disconnect
            if update_full()==False:
                logging.log(logging.INFO, "Maybe Network trouble, so wait 100 second, then open setting page again")
                time.sleep(100)#why is 100s, as sometimes, update still can go on by DUT self
                driver.quit()
                driver = webdriver.Chrome("%s\chromedriver.exe"%os.getcwd())
                driver.get(IP)
            if i==cycle:
                Run_status="Running Over"
            end=time.time()
            diff_time=int(end-start)
            #duration="%sh:%sm:%ss"%(int((end-start)/3600),int((end-start)/60),int((end-start)%60))
            duration=str(datetime.timedelta(seconds=diff_time))
            logging.log(logging.INFO, "Success update times is %d"%update_time)
            CreateHTMLRpt.report_result(title,start_time,duration,str(i),Run_status,update,str(update_time),downgrade,str(downgrade_time),'Network_Error',str(Network_Error))

    driver.quit()