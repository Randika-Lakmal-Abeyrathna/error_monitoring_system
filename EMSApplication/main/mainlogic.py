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
import tkinter as tk
from tkinter import filedialog
import random
import string

class minlogic :
    def sendEmail(to,content):
        mail_content = content
        
        sender_address = 'randika.help@gmail.com'
        sender_pass = 'euqqowwthnhdfeam'
        
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = "," .join(to)
        message['Subject'] = 'Error Summary'   #The subject line
        
        message.attach(MIMEText(mail_content, 'plain'))
        
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls() 
        session.login(sender_address, sender_pass) 
        text = message.as_string()
        session.sendmail(sender_address, to, text)
        session.quit()

    def readfillelist(fromdate,todate,configlist,selected):
        print(fromdate)
        print(todate)
        print(configlist)
        pathlist =[]
        if selected == '0':
            for con in configlist:
                pathlist.append(con)
        else:
            pathlist.append(configlist)
        
        print(pathlist)
        

        error_list = []

        for ip in pathlist:
            print(ip.path)
            path = ip.path
            pathName = ip.name
            print(pathName)
            for x in os.listdir(path):
                if x.endswith(".log") & x.startswith("laravel"):
                    # Prints only text file present in My Folder
                    dates = x.split('-')[1]+"-"+x.split('-')[2]+"-"+(x.split('-')[3]).split(".")[0]
                    date1 = fromdate
                    date2 = todate
                    file_date = datetime.strptime(str(dates),"%Y-%m-%d")
                    file_date1 = datetime.strptime(str(date1),"%Y-%m-%d")
                    file_date2 = datetime.strptime(str(date2),"%Y-%m-%d")
                    if  file_date1 <= file_date  <= file_date2:
                        with open(path+"//"+x,'r') as f:
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
                                            if (err["date"] == error_date) & (err["error_message"] == error_message_content) & (err["server_name"] == pathName):
                                                err["error_time"].append(error_dateTime)
                                                err["count"] += 1
                                                flag=True
                                                break
                                            else:
                                                flag=False
                                        
                                        if not flag:
                                            log_error ={
                                            "date":error_date,
                                            "error_time": [error_dateTime],
                                            "error_message":error_message_content,
                                            "server_name":pathName,
                                            "count":1
                                            }
                                            error_list.append(log_error)
                                        
                                    else:
                                        log_error ={
                                            "date":error_date,
                                            "error_time": [error_dateTime],
                                            "error_message":error_message_content,
                                            "server_name":pathName,
                                            "count":1
                                        }
                                        error_list.append(log_error)
        
        return error_list

    def exportFile(datalist):
        list = datalist
        df = pd.DataFrame(list)
        file_path = filedialog.askdirectory()
        print(file_path)
        writer = pd.ExcelWriter(file_path+"//"+'export.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Error Summary', index=False)
        writer.save()

    def genratepassword():
        source = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(source) for i in range(8)))
        return result_str

    
    def resetPasswordEmail(to,content):
        mail_content = 'New password is '+content
        
        sender_address = 'randika.help@gmail.com'
        sender_pass = 'euqqowwthnhdfeam'
        
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = "," .join(to)
        message['Subject'] = 'Password Reset'   #The subject line
        
        message.attach(MIMEText(mail_content, 'plain'))
        
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls() 
        session.login(sender_address, sender_pass) 
        text = message.as_string()
        session.sendmail(sender_address, to, text)
        session.quit()
