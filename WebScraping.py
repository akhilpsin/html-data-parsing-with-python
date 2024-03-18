#!/usr/bin/env python
#Importing Required Libraries
from bs4 import BeautifulSoup
import requests
import csv
import re
import requests

#This part of the code is to extract all the index JOB id for parcing
jobURLs=[]
for i in range(1,5):
    url = 'https://www.staticjobs.com/search.php?query=Canada&page='+str(i)
    page = requests.get(url,verify=False).text
    page = BeautifulSoup(page, 'html.parser')
    searcID=page.find("div", {"id":"search_results"})
    
    for box in searcID.find_all("div", {"class":"row"}):
        a=str(box.find("h1", {"class":"ellipsis"})).split("php?id=")[-1].split('''" title="''')[0]
        jobURLs.append(a)

print("Job extracted",len(jobURLs))

fields=["Job Title","Date","Location","Pay Rate","Employement type","Job Duration","Required skills","Job URL"]
with open("jobdata.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        
for job in jobURLs:
    url = 'https://www.staticjobs.com/view_job.php?id='+job
    page = requests.get(url,verify=False).text
    page = BeautifulSoup(page, 'html.parser')
    job=page.find("h1", {"id":"job_title"}).text
    job_summary=page.find("table", {"id":"job_summary"})
    job_summary=job_summary.find_all("tr")
    
    datePosted=job_summary[0].text.split("\n")[-2]
    jobLocation=job_summary[1].text.split("\n")[-2]
    payRate=job_summary[2].text.split("\n")[-2]
    employmentType=job_summary[3].text.split("\n")[-2]
    jobDuration=job_summary[4].text.split("\n")[-2]
    requiredSkills=job_summary[5].text.split("\n")[-2]
     
    with open("jobdata.csv", 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([job,datePosted,jobLocation,payRate,employmentType,jobDuration,requiredSkills,url])




