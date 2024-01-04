#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import requests
import openai
import tiktoken
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def search(query, mode="Professional", length="long"):
    if length.lower() == "long":
        length =""
    elif length.lower() == "medium":
        length='within 70 to 100 words'
    else :
        length='within 30 to 60 words'
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query,"gl":"in"})
    headers = {'X-API-KEY': '2222ec707c695b2b1bae012e31f33b4531ab4a76',
               'Content-Type': 'application/json'}
    
    urlImage = "https://google.serper.dev/images"
    payloadImage = json.dumps({"q": query,"gl": "in"})
    headersImage = {'X-API-KEY': '199dfdfde0b7d639270d75990389b3d2bb48df45',
               'Content-Type': 'application/json'}    
    
    try:
        # Make a GET request to the API
        response = requests.request("POST", url, headers=headers, data=payload)
        responseImage = requests.request("POST", urlImage, headers=headersImage, data=payloadImage)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()
            dataImage = responseImage.json()         
            if "relatedSearches" not in data:
                if "peopleAlsoAsk" in response.json():
                    relatedSearch =[i['question'] for i in response.json()['peopleAlsoAsk']][:3]
                else:
                    relatedSearch=[]
            else:
                relatedSearch = [i['query'] for i in data['relatedSearches']][:3]
            trusted_sources=["twitter","instagram","facebook","linkedin",'pib','indianexpress','timesofindia','inshorts','livemint','bbc','thewire','thequint','economictimes','hindustantimes','nytimes','theguardian','washingtonpost','cnbc','edition','abplive','firstpost','ndtv','indiatoday']
            
            social_media_sites=["quora","reddit", "youtube"]
            
            
            # All links , snippet and title
            all_links = [(i['link'], i['snippet'], i['title']) for i in data['organic'] if "snippet" in list(i.keys()) and "title" in list(i.keys()) and "link" in list(i.keys())]
            
            final_links = [i[0] for i in all_links]
            gov = [i for i in final_links if  i.split("/")[2] == "www.india.gov.in"]
            if gov:
                final_links.remove(gov[0])
                final_links.insert(0, gov[0])
                links = final_links[:5]
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                time.sleep(2)
                # Open Scrapingbee's website
                driver.get(gov[0])
                element = driver.find_element(By.CSS_SELECTOR,"#block-system-main > div")
                output_text = element.text
                description = output_text
                driver.close()
                
            else:
                # Remove social media sites from links
                for i in social_media_sites:
                    for j in all_links:
                        if i in j[0]:
                             all_links.remove(j)

                # Make new links list of trusted source and remove from old all_links variable 
                final_links = []                
                for i in trusted_sources:
                    for j in all_links:
                        if i in j[0]:
                            final_links.append(j)
                            all_links.remove(j)

                # if new links list have not 5 links so add from the old all_links

                if len(final_links) < 5:
                    final_links.extend(all_links[:5-len(final_links)]) 

                links = [i[0] for i  in final_links]
                output_text = " ".join([i[2]+" " + i[1] for i  in final_links])
                description = [i[2]+" " + i[1] for i  in final_links]
            
            
            user_content=f"According to given text:{output_text}, generate answer for the following question in {mode} way {length}: {query}"
            
            output=client.chat.completions.create(
                model="togethercomputer/Llama-2-13b-chat",
                messages=[{"role": "user", "content": user_content}],
                temperature=0.7,
                stop=['[/INST]', '</s>'],
            max_tokens= 1024)
            final_output = re.sub(r'Sure.*\n|Here.*\n|Based.*\n',"",output.choices[0].message.content.strip()).strip()
            return {"response": final_output, "links": links, "descriptions": description, "Related_Search" : relatedSearch, "images":[i['imageUrl'] for i in dataImage['images'] if "imageUrl" in list(i.keys())][:4]}

        else:
            # Handle API error responses
            return f'Error: Unable to fetch data from API (Status Code: {response.status_code})'

    except Exception as e:
        # Handle other exceptions such as network errors
        return f'Error: {str(e)}'

