# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:28:24 2021

@author: Rui
"""
import os
import io
import urllib
from urllib.request import urlretrieve
import socket
from PIL import Image
from PIL import UnidentifiedImageError 

# create img dir
# os.mkdir('./img')

socket.setdefaulttimeout(30)

# read urls
def old_ways(url, path):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/35.0.1916.114 Safari/537.36',
        'Cookie': 'AspxAutoDetectCookieSupport=1'
    }
    try:
        request = urllib.request.Request(url, None, header)
        response = urllib.request.urlopen(request)
        with open(path, "wb") as f:
            f.write(response.read())
    except:
        pass

urls = []
captions = []
with open('./cc12m.tsv',encoding='utf-8', mode='r') as f:
    for i in f.readlines():
        url, caption = i.split('\t')
        urls.append(url)
        captions.append(caption)

bad_urls = []
good_rec = []
count = 0
for url in urls:
    url.rstrip('\n')
    print(str(count),"/",str(len(urls)))
    print(url)
    attempts = 0
    success = False
    while attempts < 20 and not success:
        try:
            if not os.path.isfile('./img/%d.jpg' % count):
                urlretrieve(url, './img/%d.jpg' % count)
            # ---------img check--------------
            with open('./img/%d.jpg' % count, 'rb') as image_file:
                image_byte = image_file.read()
            image_file = io.BytesIO(image_byte)
            image = Image.open(image_file)
            image.verify()
            image_file.close()
            image.close()
            #---------------------------------
            print('pic %d downloaded' % count)
            good_rec.append(count)
            success = True
        except UnidentifiedImageError:
            print("not img error")
            os.remove('./img/%d.jpg' % count)
            bad_urls.append(str(count)+"\t"+url)
            break
        except socket.timeout:
            print("wait too long error")
            bad_urls.append(str(count)+"\t"+url)
            break
        except:
            print("error with img %d" % count, " retrying %d" % attempts)
            old_ways(url, './img/%d.jpg' % count)
            attempts += 1
            if attempts == 20:
                bad_urls.append(str(count)+"\t"+url)
                break
    count += 1

# save bad links
with open('bad_url.data', 'w', encoding='utf-8') as f:
    for i in bad_urls:
        f.write(i)
        f.write('\n')
    print('saved bad urls')

# save captions and ids
with open('cc12m.csv', 'w', encoding='utf-8') as f:
    for i in good_rec:
        f.write(i)
        f.write('\t')
        f.write(captions[i-1])
        f.write('\n')
    print('captions saved')