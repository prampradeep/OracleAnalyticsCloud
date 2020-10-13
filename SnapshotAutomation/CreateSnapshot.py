# Packages Import
import time
from time import strftime
import datetime
import os, io
import oci
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import configuration
# Chrome Options
CHROMEDRIVER_PATH = os.getcwd()+'/chromedriver'
DownloadDir = os.getcwd()+'/Snapshots'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": DownloadDir,
  "download.prompt_for_download": False,
})
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)
# Set Date 
e = datetime.datetime.now()
print("####################################################################################")
print("############################ Creating Snapshot #####################################")
print("####################################################################################")
print("### The time is: ",e.strftime("%Y-%m-%d %H:%M:%S"))
snapshotname = configuration.prefix+" - "+e.strftime("%b %d %Y %H:%M:%S %p")
print("### The Snapshot name is: ",snapshotname)
# Code for Selenium 
#driver = webdriver.Chrome()
driver.get("https://"+configuration.hostname+"/ui/sac/snapshots/Snapshots.html")
driver.set_window_size(968, 528)
WebDriverWait(driver, 300000).until(expected_conditions.element_to_be_clickable((By.ID, "idcs-signin-basic-signin-form-username")))
driver.find_element(By.ID, "idcs-signin-basic-signin-form-username").send_keys(configuration.UserName)
driver.find_element(By.ID, "idcs-signin-basic-signin-form-password").send_keys(configuration.Password)
driver.find_element(By.CSS_SELECTOR,"#idcs-signin-basic-signin-form-submit").click()
print("### Logged in to OAC")
WebDriverWait(driver, 300000).until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[contains(.,'Create Snapshot')]")))
driver.find_element(By.XPATH,"//span[contains(.,'Create Snapshot')]").click()
WebDriverWait(driver, 300000).until(expected_conditions.element_to_be_clickable((By.ID, "newName|input")))
driver.find_element(By.ID, "newName|input").send_keys(snapshotname)
driver.find_element(By.CSS_SELECTOR,"oj-button.bi-dialog-callout-button.oj-button.oj-component.oj-button-full-chrome.oj-button-text-only.oj-complete.oj-enabled.oj-default").click()
print("### Submitted Snapshot request ",snapshotname," at ",strftime("%Y-%m-%d %H:%M:%S"))
time.sleep(5)
WebDriverWait(driver, 300000).until(expected_conditions.invisibility_of_element((By.XPATH,"//*[text()='Creating...']")))
time.sleep(5)
print("### Finished Creating Snapshot"," at ",strftime("%Y-%m-%d %H:%M:%S"))
# Downloading the Created Snapshot
WebDriverWait(driver, 300000).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,"#snapshots-table")))
element_to_hover = driver.find_element(By.XPATH,"//*[text()='"+snapshotname+"']")
hover = ActionChains(driver).move_to_element(element_to_hover)
hover.context_click().perform()
WebDriverWait(driver, 300000).until(expected_conditions.element_to_be_clickable((By.XPATH,"//*[starts-with(@class, 'sacSnapshotTableMenu')]")))
driver.find_element(By.XPATH,"//*[text()='Download']").click()
WebDriverWait(driver, 300000).until(expected_conditions.element_to_be_clickable((By.XPATH,"//*[starts-with(@id, 'sacPasswordInput_ojcustomelem')]")))
driver.find_element(By.XPATH,"//*[starts-with(@id, 'sacPasswordInput_ojcustomelem')]").send_keys(configuration.SnapPassword)
driver.find_element(By.XPATH,"//*[starts-with(@id, 'sacConfirmPasswordInput_ojcustomelem')]").send_keys(configuration.SnapPassword)
driver.find_element(By.CSS_SELECTOR,"oj-button.bi-dialog-callout-button.oj-button.oj-component.oj-button-full-chrome.oj-button-text-only.oj-complete.oj-enabled.oj-default").click()
WebDriverWait(driver, 300000).until(expected_conditions.invisibility_of_element((By.XPATH,"//*[text()='Downloading snapshot...']")))
print("### File is Downloaded"," at ",strftime("%Y-%m-%d %H:%M:%S"))
time.sleep(5)
#####################################################################
####Tenancy & User details for Authentication ( Change as needed)####
#####################################################################
# Bcket Detils
namespace = configuration.namespace
bucket = configuration.bucket
# Config
config = oci.config.from_file()
ocios = oci.object_storage.ObjectStorageClient(config)
for file in os.listdir(DownloadDir):
    filename=DownloadDir+'/'+file
    print("### Uploading",snapshotname)
    ocios.put_object(namespace,bucket,snapshotname,io.open(filename,'rb'))
    print("### Upload to Object Storage Complete")
    os.remove(filename)
print("####################################################################################")
print("##################### Create Snapshot Successfull ##################################")
print("####################################################################################")
    