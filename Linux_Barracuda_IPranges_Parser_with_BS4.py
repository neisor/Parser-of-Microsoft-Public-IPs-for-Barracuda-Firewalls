# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 09:30:44 2019

@author: Antonio Raffaele Iannaccone
"""
import requests
import re
from bs4 import BeautifulSoup

#Get the HTML of the main Microsoft website with a button to download
url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=53602"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

#Find the download button on a website
soup_found_element = soup.find(class_="link-align")

#Find the link of the download button
soup_url_for_download_list = re.findall('href=\"(.*\.csv)\"', str(soup_found_element))

#Convert the regexed URL for download from a list to a string
soup_url_for_download_string = ''.join(soup_url_for_download_list)

#Download file
file_download = requests.get(soup_url_for_download_string, allow_redirects=True)

#Save the downloaded file to a specific location
open('/tmp/Barracuda_IP_ranges_CSV.csv', 'wb').write(file_download.content)

#Open the file in the buffer and perform the first regex to get only the IP ranges from the file
with open('/tmp/Barracuda_IP_ranges_CSV.csv', 'r') as file:
    lines_in_csv = file.read()
    regexed_lines_list = re.findall(r"(^.*?,)", str(lines_in_csv), re.MULTILINE)

#Convert the regexed list to string
regexed_lines_string = ''.join(regexed_lines_list)

#Perform final regexes to leave only the IP ranges in a format IPrange IPrange IPrange, etc.
regexed_lines_string_output = re.sub("(,)", " ", regexed_lines_string)
regexed_lines_string_output = re.sub("(Prefix )", "", regexed_lines_string_output)

#Save the output file with only the IP ranges to a specific location
f = open('/tmp/Barracuda_Output_IPranges.txt', 'w')
f.write(str(regexed_lines_string_output))
f.close()