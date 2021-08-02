'''
Replicate remote directory structure on local machine with recursion
Only copy directory structure and files ending in ".fits" extension
'''
from bs4 import BeautifulSoup
import requests
import os

def url_download_recur(base_url, dir_name):
    try:
        path = os.path.join(os.getcwd(), dir_name[:-1])
        print(path)
        if not os.path.exists(dir_name[:-1]): # make new directory if it doesn't already exist
            os.system("mkdir " + dir_name[:-1])
        os.chdir(dir_name[:-1]) # switch to new directory
        html_text = requests.get(base_url).text
        soup = BeautifulSoup(html_text, "lxml")
        div_container = soup.find("tbody")
        if div_container == None:
            return
        for tag in div_container.find_all("a"):
            if tag.text.endswith(".fits"): # found fits file
                print("FITS File Found: " + base_url + tag.text)
                os.system("wget " + base_url+tag.text) # CALL WGET COMMAND
            elif not(tag.text == "Parent directory/") and not("." in tag.text): # found a directory
                print("Subdirectory Found: " + base_url + tag.text)
                url_download_recur(base_url+tag.text, tag.text) # RECURSE DOWN SUBDIRECTORIES
                os.chdir(path)
    except Exception as e:
        os.system("Echo Error: " + e)

# call base link
#url_download_recur("https://data.sdss.org/sas/dr13/sdss/tiling/final/", "final/")
#url_download_recur("https://data.sdss.org/sas/dr13/sdss/", "sdss/")
#url_download_recur("https://data.sdss.org/sas/dr13/sdss/target/", "target/")
