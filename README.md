# MP3_beautifier

Ce programme permet à partir d'un dossier rempli de fichier de musique ayant des noms signifiant de retrouver les données de la musique (titre, artiste, album, année, genre) et de les mettre dans les métadonnées du fichier MP3.

## Fonctionnement

Le programme utilise pour l'instant du scraping sur Google afin de récupérer le "résultat zéro" de Google : 

![Image des résultats zéros de Google, donnant toutes les données sur la chanson "Aux Champs-Élysées" (titre exact, date de sortie, artiste, album, genre, etc.)](docs/ZeroGoogle.png)

### Scraping des informations

Le scraping est réalisé dans la fonction *song.get_metadata*

Le scraping commence par une recherche avec le nom complet du fichier MP3, si cela ne donne aucun résultat les mots sont retirés de la fin au fur et à mesure, c'est bien souvent ici qu'on trouve des informations inutiles ou les watermark des différents sites de téléchargement.

### Téléchargement des pochettes d'album

Le téléchargement des pochettes d'album est réalisé dans la fonction *song.get_album_art*, elle passe par *bing images*.

## Utilisation

### Installation

Pour installer le programme, il suffit de cloner le dépôt et d'installer les dépendances avec pip :
    
```pip install -r requirements.txt```

### Utilisation

Pour utiliser le programme, il suffit de lancer le fichier *gui.py* avec python :

```python3 gui.py```