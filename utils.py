from distutils import extension
import os
import shutil
import urllib
import requests
from requests_html import HTMLSession
import tqdm
import bs4

def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)

def clean_beautiful():
    for file in os.listdir('beautiful'):
        os.remove('beautiful/' + file)

#Copie des fichiers de ugly dans beautiful

def copy_beautiful():
    bar = tqdm.tqdm(total=len(os.listdir('ugly')))
    for file in os.listdir('ugly'):
        shutil.copy('ugly/' + file, 'beautiful/' + file)
        bar.update(1)
    bar.close()

#Récupération du code source d'une page google à partir de la recherche

def get_source_google(search : str):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """
    search = urllib.parse.quote(search)
    url = "https://www.google.com/search?channel=fs&client=windows&q=" + search
    try:
        session = HTMLSession()
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

#Retire le derner mot d'une chaine de caractère

def back_from_one_space(text):
    if len(text) == 0:
        return None
    i = -1
    while i != -len(text) and text[i] != ' ':
        i -= 1
    if i == -len(text):
        return None
    return text[:i]

def get_first_image(artiste,album):
    url="https://www.bing.com/images/search?q="+urllib.parse.quote(artiste+" "+album)+"&form=HDRSC2&first=1&tsc=ImageHoverTitle"
    try:
        session = HTMLSession()
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"} 
        response = session.get(url,headers=headers)

    except requests.exceptions.RequestException as e:
        exit()
    soup=bs4.BeautifulSoup(response.content,"html.parser")

    finished = False
    index = 1
    while not(finished):
        try:
            element = soup.find('li',attrs={'data-idx':str(index)})
            image_url = element.find('img', attrs={'class':'mimg'})['src']
            
            #download image
            img_data = requests.get(image_url).content
            with open('album/'+remove_non_ascii(artiste.lower()+album.lower())+'.jpg', 'wb') as handler:
                handler.write(img_data)
            finished = True
        except requests.exceptions.InvalidSchema:
            #The file is encoded in base64
            print("image en base64 : décryptage")
            code = element.find('img', attrs={'class':'mimg'})['src']
            if "data:image" in code:
                extension = code[11:]
                index = 0 
                while extension[index] != ";":
                    index += 1
                extension = extension[:index]
                print("Extension : " + extension)
                code = code[index+12+7:]
                print(code)
        except KeyError:
            print("No image found")
        index+=1
if __name__ == "__main__":
    get_first_image("eminem","recovery")
