from enum import Flag
from unicodedata import name
import urllib
import re
from datetime import date, datetime
from datetime import timedelta
import csv
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os
import glob
from os.path import exists

class minlogic :
    def sendEmail():
        yesterday = date.today() - timedelta(days=1)
        yd = yesterday.strftime("%Y-%m-%d")

        files = glob.glob(yd+"/*.csv")
        smtpServer = ''
        recipients =['randika.help@gmail.com']

        msg = MIMEMultipart()
        body_part = MIMEText("Error log for "+ yd , 'plain')
        msg['Subject'] = 'Error Log Summary for : '+yd
        msg['From'] = 'randika.help@gmail.com'
        msg['To'] = "," .join(recipients)
        msg.attach(body_part)

        for f in files:
            x= f.split("\\")[1]
            with open(f,'rb') as file:
                msg.attach(MIMEApplication(file.read, name=x))

        smtp_obj = smtplib.SMTP(smtpServer)
        smtp_obj.starttls()
        smtp_obj.sendmail(msg['From'],recipients,msg.as_string)
        smtp_obj.quit()

    def readfillelist():
        error_list = []
        path = "C://Users//randi//Downloads//Log//Log"
        aligibale_file_list =[]
        for x in os.listdir(path):
            if x.endswith(".log") & x.startswith("laravel"):
                # Prints only text file present in My Folder
                dates = x.split('-')[1]+"-"+x.split('-')[2]+"-"+(x.split('-')[3]).split(".")[0]
                date1 = '2022-09-01'
                date2 = '2022-10-06'
                file_date = datetime.strptime(str(dates),"%Y-%m-%d")
                file_date1 = datetime.strptime(str(date1),"%Y-%m-%d")
                file_date2 = datetime.strptime(str(date2),"%Y-%m-%d")
                if  file_date1 <= file_date  <= file_date2:
                    aligibale_file_list.append(x)

        error_list = []
        # print(aligibale_file_list)
        for file in aligibale_file_list:
            # print(file)
            with open(path+"//"+file,'r') as f:
                lines = f.readlines()
                count = 0
                # Strips the newline character
                for line in lines:
                    if "production.ERROR" in line.strip():
                        error_message = line.strip()
                        error_message_parts = line.strip().split('production.ERROR')
                        error_dateTime = error_message_parts[0]
                        error_message_content = error_message_parts[1].split(':')[1]
                        error_date = error_dateTime.split(" ")[0].replace('[',"")
                        # print(error_date)
                        
                        if len(error_list):
                            flag =False
                            for err in error_list:
                                if (err["date"] == error_date) & (err["error_message"] == error_message_content):
                                    err["error_time"].append(error_dateTime)
                                    err["count"] += 1
                                    print("same Date same content")
                                    flag=True
                                    break
                                else:
                                    flag=False
                            
                            if not flag:
                                log_error ={
                                "date":error_date,
                                "error_time": [error_dateTime],
                                "error_message":error_message_content,
                                "count":1
                                }
                                error_list.append(log_error)
                            
                        else:
                            log_error ={
                                "date":error_date,
                                "error_time": [error_dateTime],
                                "error_message":error_message_content,
                                "count":1
                            }
                            error_list.append(log_error)
                            print("first")
                        # print("Line{}: {}".format(count, line.strip()))
        print(error_list)
        return error_list

    def send_singlelog(serUrl,servername):
        yesterday = date.today() - timedelta(days=1)
        yd = yesterday.strftime("%Y-%m-%d")

        logLink =serUrl+'error.'+yd+".0.log"

        f = urllib.request.urlopen(logLink)
        myfile = f.read()

        myfile_text = myfile.decode("utf-8")

        myfile_list = myfile_text.split("\n")

        index =0 

        errorlog_list =[]

        while index < len(myfile_list) :
            myfile_line = myfile_list[index]
            if (myfile_line.startswith('202')):
                errorlog_list.append(myfile_line)
            index +=1
        
        eindex =0
        col=0
        errorlogwiod_list=[]
        errorwithod_list=[]
        error_dic = {"col":[],"date":[],"log":[]};

        while eindex <len(errorlog_list):
            errorlogwiod_list = errorlog_list[eindex].split(" - ",1)
            if(errorlogwiod_list[1] not in errorwithod_list):
                error_dic["col"].append(col)
                error_dic["date"].append(errorlogwiod_list[0])
                error_dic["log"].append(errorlogwiod_list[1])
                errorwithod_list.append(errorlogwiod_list[1])
                col +=1
            eindex +=1

        
        error_pand = pd.DataFrame(error_dic)
        print(error_pand)

        opFileName = yd+'/error_'+servername+'.csv'
        error_pand.to_csv(opFileName,encoding='utf-8',index=False)


    def send_Multilog(serUrl,servername,noFiles):
        yesterday = date.today() - timedelta(days=1)
        yd = yesterday.strftime("%Y-%m-%d")

        errorlog_list = []
        no_files = 0

        while noFiles>no_files:
            logLink =serUrl+'error.'+yd+"."+str(no_files)+".log"

            f = urllib.request.urlopen(logLink)
            myfile = f.read()

            myfile_text = myfile.decode("utf-8")

            myfile_list = myfile_text.split("\n")

            index =0 

            while index < len(myfile_list) :
                myfile_line = myfile_list[index]
                if (myfile_line.startswith('202')):
                    errorlog_list.append(myfile_line)
                index +=1
            no_files +=1

        eindex =0
        col=0
        errorlogwiod_list=[]
        errorwithod_list=[]
        error_dic = {"col":[],"date":[],"log":[]};

        while eindex <len(errorlog_list):
            errorlogwiod_list = errorlog_list[eindex].split(" - ",1)
            if(errorlogwiod_list[1] not in errorwithod_list):
                error_dic["col"].append(col)
                error_dic["date"].append(errorlogwiod_list[0])
                error_dic["log"].append(errorlogwiod_list[1])
                errorwithod_list.append(errorlogwiod_list[1])
                col +=1
            eindex +=1

        
        error_pand = pd.DataFrame(error_dic)
        print(error_pand)

        opFileName = yd+'/error_'+servername+'.csv'
        error_pand.to_csv(opFileName,encoding='utf-8',index=False)

    #  Calling Logic 

    def callingLogic():
        yesterday = date.today() - timedelta(days=1)
        yd = yesterday.strftime("%Y-%m-%d")

        isExists= exists(yd)

        if not isExists:
            os.mkdir(yd)

        serName=[]
        portNo=''

        serno=0
        while (serno <2):
            serUrl = "http://"+serName[serno]+':'+portNo+'/logs/archived/'

            try:
                html_content = urllib.request.urlopen(serUrl).read().decode("utf-8")
            except urllib.error.HTTPError as e:
                print('HTTP Error occured: '+e.__dict__)
                exit()
            except urllib.error.URLError as e:
                print('URL Error occured: '+e.__dict__)
                exit()

            matches = re.findall('error.'+yd,html_content)

            if len(matches) == 0:
                print("There are no log files")
            else:
                noFiles = (len(matches))/2

                if (noFiles == 1):
                    send_singlelog(serUrl,serName[serno])
                elif (noFiles > 1):
                    send_Multilog(serUrl,serName[serno],noFiles)

            serno +=1



