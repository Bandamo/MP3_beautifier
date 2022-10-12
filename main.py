import eyed3
import os
import tqdm
import shutil
import requests
import urllib
import bs4
from requests_html import HTMLSession
import time


liste_artiste=[]
liste_album=[]

class song:
    def __init__(self, old_title : str):
        self.old_title = old_title
        self.title = "None"
        self.artist = "None"
        self.album = "None"
        self.date = "None"
        self.album_art = "None"
    
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
            if self.album_art != "None":
                audiofile.tag.images.set(3, open("album/"+self.album_art, 'rb').read(), 'image/jpeg')
            
            try:
                audiofile.tag.save()
            except:
                print("Error while saving tag")
                pass

    def get_metadata(self,text,liste_artiste,liste_album):

        #Get the response from google
        response = get_source_google(text).text
        soup = bs4.BeautifulSoup(response, 'html.parser') #HTML page parsed

        found=False

        #Check if the song is in the first page of google
        if not(len(soup.find_all('div',attrs={'data-attrid':'kc:/music/recording_cluster:artist'}))==0 and len(soup.find_all('div',attrs={'data-attrid':'kc:/music/recording_cluster:album'}))==0 and len(soup.find_all('div',attrs={'data-attrid':'kc:/music/recording_cluster:release_date'}))==0):
            found=True
            title = soup.find_all('div',attrs={'class':'PyJv1b gsmt PZPZlf','data-attrid':'title'})
            if len(title)==0:
                print('No title found')
            else:
                print("Titre : " + title[0].text)
                self.title = title[0].text
            
            artist_found = False
            for elem in liste_artiste:
                if elem.lower() in text.lower():
                    artist_found = True
                    self.artist = elem
                    print("Artiste : " + elem)
                    break
            if artist_found == False:
                artist = soup.find_all('div',attrs={'data-attrid':'kc:/music/recording_cluster:artist'})
                if len(artist)==0:
                    print('No artist found')
                else:
                    print("Artiste : " + artist[0].text[10:])
                    self.artist = artist[0].text[10:]
                    liste_artiste+=[artist[0].text[10:]]


            album_found = False
            for elem in liste_album:
                if elem.lower() in text.lower():
                    album_found = True
                    self.album = elem
                    print("Album : " + elem)
                    break
            if album_found == False:
                album = soup.find_all('div',attrs={'data-attrid':'kc:/music/recording_cluster:first album'})
                if len(album)==0:
                    print('No album found')
                else:
                    print("Album : " + album[0].text[8:])
                    self.album = album[0].text[8:]
                    liste_album+=[album[0].text[8:]]
            
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
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 
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

def main():
    clean_beautiful()
    copy_beautiful()
    print('Copie terminée')
    liste_song = os.listdir('beautiful')
    liste_song.sort()
    print("Liste des chansons évaluées, "+str(len(liste_song))+" chanson(s) trouvée(s).")

    liste_artiste=[]
    liste_album=[]

    bar=tqdm.tqdm(total=len(os.listdir('beautiful')))
    for s in liste_song:
        s=s[:-4]
        bar.update(1)
        print(s)
        Song = song(s)
        Song.get_metadata(s,liste_artiste,liste_album)
        try:
            Song.update_tag()
        except:
            pass
        time.sleep(0.5)

if __name__=='__main__':
    main()