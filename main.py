import eyed3
import os
import tqdm
import shutil

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


if __name__=='__main__':
    clean_beautiful()
    copy_beautiful()