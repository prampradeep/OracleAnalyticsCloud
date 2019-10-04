################################################################################
# Copyright(c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.
# StopOAC.py
#
# @author: Rampradeep Pakalapati
#
# Supports Python 3 and above
#
# coding: utf-8
#################################################################################
# PSMCLI Tool:
#
# requires a payload file for IDCS authentication:
# User should have service Administration Role to control Oracle Analytics Cloud Instances
#
# config file should contain:
#     [TENANT_NAME]
#     username 			=	IDCS username 
#     password 			= 	IDCS Password
#     Identity Domain  	=   IDCS account ID
#     region 			=   us,emea or aucom
#     output Format		=   short, json or html
#
# Example payload file below:
#		{ 
#			"username":"rampradeep.pakalapati@oracle.com",
#			"password":"xxxxxxxxxxxxxxx",
#			"identityDomain":"idcs-xxxxxxxxxxxxxxxxxxxxxxxxx",
#			"region":"us",
#			"outputFormat":"json"
#		}
#
##########################################################################
#
# Available Services via PSMCLI are:
#
# - accs : Oracle Application Container Cloud Service
# - ADBC : Oracle Autonomous Database Cloud
# - ADWC : Oracle Autonomous Data Warehouse Cloud
# - ADWCP : Oracle Autonomous Data Warehouse Cloud Platform
# - AIACS : Oracle Adaptive Intelligent Cloud Service AIACS
# - AIPOD : Oracle Adaptive Intelligent Cloud Service POD
# - ANALYTICS : Oracle Analytics Cloud Classic
# - ANALYTICSSUB : Oracle Analytics Cloud Subscription
# - ANDC : Oracle Autonomous NoSQL Database Cloud Service
# - ANDCP : Oracle Autonomous NoSQL Database Cloud Pod
# - APICatalog : Oracle API Catalog Service
# - APICS : Oracle API Platform Cloud Service - Classic
# - APICSAUTO : Oracle API Platform Cloud Service
# - APICSAUTOPOD : Oracle API Platform Cloud Service Pod
# - APISearch : Oracle APICatalog Elasticsearch Service
# - AUTOANALYTICS : Oracle Analytics Cloud
# - AUTOANALYTICSINST : Oracle Analytics Cloud
# - AUTOANALYTICSPOD : Oracle Autoanalytics Pod
# - AUTOBLOCKCHAIN : Oracle Autonomous Blockchain Cloud Service
# - BCSCA : Oracle BCS CA
# - BCSCBC : Oracle BCS Manager
# - BCSCONSOLE : Oracle BCS Console
# - BCSMGR : Oracle BCS Manager
# - BCSMGRPOD : Oracle BCS Manager Pod
# - BDCSCE : Oracle Big Data Cloud
# - BigDataAppliance : Oracle Big Data Cloud Service
# - BOTMXP : Oracle Autonomous Mobile Cloud Bots Service Platform
# - BotSaaSAuto : Oracle Digital Assistant
# - BOTSCFG : Oracle Bots Configuration Service
# - BOTSCON : Oracle Bots Connector Service
# - BOTSINT : Oracle Bots Intent Service
# - BOTSMGM : Oracle Bots Management API Service
# - BOTSPIP : Oracle Bots Pipeline Service
# - BOTSXP : Oracle Autonomous Digital Assistance Platform
# - caching : Oracle Application Cache
# - CEC : Oracle Content and Experience Cloud Pod Classic
# - CECAUTO : Oracle Content and Experience Cloud Pod
# - CECS : Oracle Content and Experience Cloud Classic
# - CECSAUTO : Oracle Content and Experience Cloud
# - commercecloud : Oracle Cloud Commerce Service
# - CONTAINER : Oracle Container Cloud Service
# - containerPod : Oracle Container Cluster Service
# - CXAANA : Oracle CxA Analytics Service
# - CXACFG : Oracle CxA Configuration Service
# - CXACOL : Oracle CxA Collector Service
# - CXAPOD : Oracle CxA Pod Cloud Service
# - dbcs : Oracle Database Cloud Service
# - DevServiceApp : Oracle Developer Cloud Service Classic
# - DevServiceAppAUTO : Oracle Developer Cloud Service
# - DevServicePod : Oracle Developer Cloud Service POD
# - DevServicePodAUTO : Oracle Developer Cloud Service POD
# - DHCS : Oracle Data Hub Cloud Service
# - dics : Oracle Data Integration Platform Cloud Service Classic
# - DIPCAUTO : Oracle Autonomous Data Integration Platform Cloud
# - DIPCINST : Oracle Data Integration Platform Cloud
# - DIPCPOD : Oracle Data Integration Platform Cloud
# - ERP : Oracle Fusion Applications
# - ggcs : Oracle GoldenGate Cloud Service
# - INTEGRATIONCAUTO : Oracle Integration
# - IntegrationCloud : Oracle Integration Classic
# - IOTAssetMon : Oracle IoT Asset Monitoring Cloud Service
# - IOTConnectedWrker : Oracle IoT Connected Worker Cloud Service
# - IOTEnterpriseApps : Oracle Internet of Things Cloud - Enterprise
# - IOTFleetMon : Oracle IoT Fleet Monitoring Cloud Service
# - IOTJLS : Oracle Internet of Things Cloud - Web
# - IOTProdMonitoring : Oracle IoT Production Monitoring Cloud Service
# - IOTSvcAsset : Oracle IoT Asset Monitoring CX Cloud Service
# - jcs : Oracle Java Cloud Service
# - KMCS : Oracle Key Management Cloud Service
# - KMCSP : Oracle Key Management Cloud Service Platform
# - MobileCCC : Oracle Mobile Custom Code Container
# - MobileCccOm : Oracle Mobile Custom Code Container Oracle-managed
# - MobileCorePOD : Oracle Mobile Core POD
# - MobileCorePodOm : Oracle Mobile Core POD Oracle-managed
# - MobileServiceAuto : Oracle Autonomous Mobile Cloud Enterprise
# - MobileStandard : Oracle Mobile Hub
# - MobileStdCcc : Oracle Mobile Custom Code Container Oracle-managed
# - MobileStdCore : Oracle Mobile Core POD Oracle-managed
# - MySQLCS : Oracle MySQL Cloud Service
# - OABCSINST : Oracle Blockchain Platform
# - OABCSPOD : Oracle Blockchain Cloud Service
# - OAICS : Oracle Adaptive Intelligence Applications Offers Cloud Service
# - OBCS : Oracle Blockchain Cloud Service
# - OEHCS : Oracle Event Hub Cloud Service
# - OEHPCS : Oracle Event Hub Cloud Service - Dedicated
# - OICINST : Oracle Integration
# - OICPOD : Oracle Integration
# - OICSUBINST : Oracle Integration for Oracle SaaS
# - OMCE : Oracle Mobile Cloud Metering Service
# - OMCEXTERNAL : Oracle Management Cloud Service
# - OMCP : Oracle Management Cloud Platform Service
# - RATSControlPlane : Oracle RATS Service
# - SEARCH : Oracle Search Cloud Service
# - SEARCHCLOUDAPP : Oracle Search Cloud Service App
# - SOA : Oracle SOA Cloud Service
# - SSI : Oracle Self-Service Integration Cloud Service
# - SSIP : Oracle Self-Service Integration Platform
# - stack : Oracle Cloud Stack Manager
# - VBINST : Oracle Visual Builder
# - VBPOD : Oracle Visual Builder
# - VisualBuilder : Oracle Visual Builder Classic
# - VISUALBUILDERAUTO : Oracle Visual Builder
# - wtss : Oracle Web Tier Security Service
#
##########################################################################
import os
import json
import pandas as pd
from pandas.io.json import json_normalize

# PSM setup to be done via a payload file (refer to line 24 for sample)
os.system('psm setup -c D:\Learning\OCI\PythonSDK\psmcli\psm-setup-payload.json')

print("......................... The Program Starts Here....................................")
print("\n")
os.system('cls' if os.name == 'nt' else 'clear')

# List all the Oracle Analytics Instances in the tenancy and convert load as JSON 
response = os.popen('psm autoanalyticsinst services').read()
da = json.loads(response)
dat1 = da['services']
head = dat1.keys()
length = len(list(head))
df = pd.DataFrame([])

# Loop to select each service, Normalize JSON and append to the pandas dataframe
for i in range(0,length):
    row = dat1[list(head)[i]]
    df = df.append(json_normalize(row),sort=False)
    df2 = df[['tags.items']]
    df2 = df2.rename(columns = {"tags.items":"strip"})
    df2['strip'] = df2['strip'].astype(str)
    df2["strip"] = df2["strip"].str.strip('[]{}')
    df['TagKey'] = df2

# Extract TagKey from the tags.items string
df = df[['serviceName','TagKey','state']]
df2 = df['TagKey'].str.split(pat = ":", n=3 ,expand=True)
df2 = df2[1].str.split(pat= "," ,n=2,expand = True )
df2 = df2[0].str.strip(" '")
df['TagKey'] = df2
print(".......Below are the OAC instances available in tenancy................................")
print("\n")
print(df)
print("\n")
print(".......................................................................................")
print(".......................................................................................")
print("\n")
#Filtering Business Analytics Instances which are currently in READY state
dfinstances = df[(df['TagKey'] == 'BAnalytics') & (df['state'] == 'READY')]
print(".......Below are the Business Analytics Instances which are in READY state ............")
print("\n")

# Converting pandas dataframe column to list 
dflist =  dfinstances['serviceName'].tolist()
print(dflist)

print(".......................................................................................")
print(".......................................................................................")
print(".........................Below are the stop commands...................................")
print("\n")

# Stopping each Oracle Analytics Cloud instance 
for i in range(0,len(dflist)):
    instance = dflist[i]
    print("Stopping the instance #",i+1,":",instance)
    stop_cmd = 'psm autoanalyticsinst stop-service -s '+instance
    print(stop_cmd)
    print("\n")
    rep = os.popen(stop_cmd).read()
    print(rep)
    print("\n")

print(".........................Program Ends Here.............................................")
print("\n")











