import eyed3
import os
import tqdm
import bs4
from requests_html import HTMLSession
import time
import utils


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
        audiofile = eyed3.load('beautiful/'+self.old_title+'.mp3')
        
        if self.title != "None":
            audiofile.tag.title = self.title
            if self.artist != "None":
                print("Updating title")
                audiofile.tag.artist = self.artist  
            if self.album != "None":
                audiofile.tag.album = self.album
            if self.date != "None":
                audiofile.tag.release_date = self.date
            if self.album_art != "None":
                audiofile.tag.images.set(3, open("album/"+self.album_art, 'rb').read(), 'image/jpeg')
                print("Album art added")
            try:
                audiofile.tag.save()
            except:
                print("Error while saving tag")
                pass
        else:
            print("No metadata found")

    def get_metadata(self,text,liste_artiste,liste_album):

        #Get the response from google
        response = utils.get_source_google(text).text
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
        else:
            print("No metadata found, trying with "+utils.back_from_one_space(text))
            try:
                self.get_metadata(utils.back_from_one_space(text),liste_artiste,liste_album)
            except TypeError:
                print("No metadata found after all, skipping")
                f=open("song.log","a")
                f.write(self.old_title+"\n")
                f.close()

    def get_album_art(self):
        if self.album == "None" or self.artist == "None":
            return 0
        elif utils.remove_non_ascii(self.artist.lower()+self.album.lower())+".jpg" in os.listdir("album"):
            print("Album art already downloaded")
            self.album_art = utils.remove_non_ascii(self.artist.lower()+self.album.lower())+".jpg"
        else:
            print("Downloading album art")
            utils.get_first_image(self.artist,self.album)
            self.album_art = utils.remove_non_ascii(self.artist.lower()+self.album.lower())+".jpg"

def main():
    utils.clean_beautiful()
    utils.copy_beautiful()
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
        Song.get_album_art()
        try:
            Song.update_tag()
        except TypeError:
            print("Error while updating tag")
            pass
        time.sleep(0.5)

if __name__=='__main__':
    main()