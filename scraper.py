# Python script to extract attributes of phone models

import requests as req
from time import sleep
import pandas as pd
from random import randint
from bs4 import BeautifulSoup as soup

# Getting HTML data by sending request
def Souping(sub_url):

    url = "https://www.gsmarena.com/" + sub_url

    try:
        # Headers to look like we are a browser
        headers = { 'User-Agent': 'Chrome/83.0.4103.97' }
        site_req = req.get(url, headers=headers)
        web_data = soup(site_req.content,'html5lib')
        return web_data

    except Exception:
        print("Error: Check your network connection and try again!!!")
        exit()


def data_to_list(data):
    
    # list to take in [ brands/models, links ] 
    list = []
    li_list = data.find_all('li')
    for li in li_list:
        a = li.find('a')
        if (a.find_all('img')):
            for feature in a.find_all('img'):
                img_title_list = feature['title'].split(' ')
                for value in range(len(img_title_list)):
                    if img_title_list[value] == 'Features':
                        # just taking phone models based on screen size
                        # removing watches and tablets
                        if 1.8 <= float(img_title_list[value+1].replace("″",'')) <= 6.7:
                            temp = [a.text, a['href']]
                            list.append(temp)
        else:
            temp = [a.text, a['href']]
            list.append(temp)

    return list

# Function to extract mobile brands
def Mobile_brands():

    # taking brand names from homepage of GSMArena
    brand_web_data = Souping('')
    brands_data = brand_web_data.find(class_="brandmenu-v2 light l-box clearfix")
    brands_list = data_to_list(brands_data)
    
    Brand_models(brands_list)

# Function to extract Models in particular brand
def Brand_models(brand_list):

    for brand in brand_list:
        models_html = Souping(brand[1])
        models_data = models_html.find(class_="makers")
        models_list = data_to_list(models_data)
        print("Scraping data from",len(models_list),"phone models in",brand[0])
        sleep(6) # Pause for loop

        Specifications(models_list)

# Function to extract specifications 
def Specifications(models_list):
    
    spec_list = []

    # Atrributes which are been taken
    di = {"modelname":"None", "nettech":"None", "status":"None", "dimensions":"None", "weight":"None", "displayresolution":"None", "displaysize":"None",
         "os":"None", "chipset":"None", "cpu":"None", "gpu":"None", "internalmemory":"None", "cam1modules":"None", "cam2modules":"None", "wlan":"None", 
         "gps":"None", "batdescription1":"None" }

    for model in models_list:
        data = Souping(model[1])
        model_name = data.find("h1",{"data-spec":"modelname"}).text
        print("Scraping data currently for model:",model_name)
        models_data = data.find("div", {"id":"specs-list"})
        for i in range(len(models_data.find_all('table'))):
            table=models_data.find_all('table')[i]
            for j in table.find_all('tr'):
                for key in di.keys():
                    for k in j.find_all(["td","a"],{"data-spec":key}):
                        di[key] = k.text
                di['modelname'] = model_name
        list = [value for value in di.values()]
        spec_list.append(list)
        # random pauses so it won't appear kind of appear
        # we are extracting data using a program
        sleep(randint(6,10)) 

        list_to_dataframe(spec_list) 

# function to list to df and write in a csv file 
def list_to_dataframe(spec_list):

    obj = pd.DataFrame(spec_list)
    obj.columns = ["Model Name", "Network Tech", "Release", "Dimensions", "Weight", "Display Resolution", "Display Size",
                    "OS", "Chipset", "CPU", "GPU", "Internal Memory", "Camera 1 Modules", "Camera 2 Modules", "WLAN", 
                    "GPS", "Battery Description"]
    obj.to_csv('specs.csv', index=False)


# Main program
if __name__ == "__main__":
    
    try:
        print("Note: Press Ctrl+C to interrupt the program as it will be scraping all phone models.")
        Mobile_brands()

    except KeyboardInterrupt:
        print("\nError: Keyboard Interruption")
