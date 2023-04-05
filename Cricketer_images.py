import urllib.request

import os

os.mkdir('./data')


def download_img(cricketer,url,img_num):
    urllib.request.urlretrieve(url,'./data/'+cricketer+' images/'+cricketer+img_num+'.png')

cricketer = 'Virat kohli'

os.mkdir('./data/'+cricketer+' images')
for i,j in enumerate(virat_images):
    download_img(cricketer,j,str(i))
    
