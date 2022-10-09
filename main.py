from tkinter import E
import eyed3
import os
import tqdm
import shutil
import requests
import urllib
import bs4
from requests_html import HTMLSession
import eyed3

class song:
    def __init__(self, old_title : str):
        self.old_title = old_title
        self.title = "None"
        self.artist = "None"
        self.album = "None"
        self.date = "None"
    
    def update_tag(self):
        audiofile = eyed3.load('beautiful/'+self.old_title)
        if self.title != "None":
            audiofile.tag.title = self.title
        else:
            if self.artist != "None":
                audiofile.tag.artist = self.artist  
            if self.album != "None":
                audiofile.tag.album = self.album
            if self.date != "None":
                audiofile.tag.release_date = self.date
            try:
                audiofile.tag.save()
            except:
                print("Error while saving tag")
                pass

    def get_metadata(self,text):
        response = get_source_google(text).text
        soup = bs4.BeautifulSoup(response, 'html.parser')
        title = soup.find_all('span',attrs={'class':'yKMVIe','aria-level':'1','role':'heading'})
        if len(title)==0:
            print('No title found')
            print(response)
            try:
                return self.get_metadata(back_from_one_space(text))
            except:
                print(text)   
                return None 
        else:
            print("Titre : " + title[0].text)
            self.title = title[0].text
        
        artist = soup.find_all('div',attrs={'data-attrid':'kc:/music/recording_cluster:artist'})
        if len(artist)==0:
            print('No artist found')
        else:
            print("Artiste : " + artist[0].text[10:])
            self.artist = artist[0].text[10:]

        album = soup.find_all('div',attrs={'data-attrid':'kc:/music/recording_cluster:first album'})
        if len(album)==0:
            print('No album found')
        else:
            print("Album : " + album[0].text[8:])
            self.album = album[0].text[8:]
        
        date = soup.find_all('div',attrs={'data-attrid':'kc:/music/recording_cluster:release date'})
        if len(date)==0:
            print('No date found')
        else:
            print("Date : " + date[0].text[17:])
            self.date = date[0].text[17:]

#Suppression des fichiers dans beautiful

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
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def back_from_one_space(text):
    if len(text) == 0:
        return None
    i = -1
    while i != len(text) and text[i] != ' ':
        i -= 1
    if i == len(text):
        return None
    return text[:i]

if __name__=='__main__':
    #clean_beautiful()
    #copy_beautiful()
    print('Copie terminée')
    liste_song = os.listdir('ugly')
    bar=tqdm.tqdm(total=len(os.listdir('ugly')))
    for s in liste_song:
        s=s[:-4]
        bar.update(1)
        print(s)
        Song = song(s)
        Song.get_metadata(s)
        try:
            Song.update_tag()
        except:
            pass