#! usr/bin/python/

import requests
import xml.etree.ElementTree as ET 
from hurry.filesize import size
import datetime
import os

logPath = "C:\\Users\\U0080217\\Documents\\_JAPAN FILINGS\\PDFFileSize\\fileLogSize.txt"
with open(logPath, "a") as text_file:
    text_file.write(str(datetime.datetime.now()) + ": start SOLR partial update" + "\n")

query = "" #provide query with SOLR URL
response = requests.get(query)
f = open("response.xml", "wb")
f.write(response.content)
f.close()

tree = ET.parse("response.xml")
root = tree.getroot()

for result in root.iter("result"):
    numFound = result.attrib["numFound"]
    if numFound != 0:
        for doc in result:
            for child in doc:
                if child.attrib["name"] == "filings_doc_id":
                    docid = child.text
                    with open(logPath, "a") as text_file:
                        text_file.write("DOC ID = " + docid + "\n")
                if child.attrib["name"] == "tr_rx_date":
                    date = child.text
                    with open(logPath, "a") as text_file:
                        text_file.write("Date Received = " + date + "\n")
                if child.attrib["name"] == "id":
                    id = child.text                   
                if child.attrib["name"] == "url":
                    url = child.text.replace("/", "%2F")
                    pdf_url = "" + url #provide server location of PDF
                    with open(logPath, "a") as text_file:
                        text_file.write("PDF URL = " + pdf_url + "\n")
                    r = requests.head(pdf_url)
                    file_size = r.headers["content-length"]
                    with open(logPath, "a") as text_file:
                        text_file.write("File Size = " + file_size + "\n")
            updateURL = "/update?commit=true" #provide SOLR URL 
            updateDATA = '[{"id":"' + id + '","filingsfilelength":{"set":"' + file_size + '"}}]'
            updateHEADERS = {'Content-type':'application/json'}
            try:
                runUpdate = requests.post(url=updateURL,data=updateDATA,headers=updateHEADERS)
                with open(logPath, "a") as text_file:
                        text_file.write("Partial update successful!" + "\n")
            except:
                with open(logPath, "a") as text_file:
                        text_file.write("Partial update failed." + "\n")
