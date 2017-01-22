#from keras.applications.resnet50 import ResNet50
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input, decode_predictions
import numpy as np
import pdb
import os
from os import listdir
from os.path import isfile, join
from gensim.models import Word2Vec
import pdb
from gensim.models import Word2Vec
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json
import logging
import datetime

IMAGE_DIR = '/Users/joeybose/Desktop/hackathon/images'

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def logElapsedTime(elapsedTime, message):
    ''' Logs the elapsedTime with a given message '''
    hours, remainder = divmod(elapsedTime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    totalDays = elapsedTime.days
    logging.info(str(message) + ': Days: ' + str(totalDays) +  " hours: " + str(hours) + ' minutes: ' + str(minutes) +  ' seconds: ' + str(seconds))

def logTimeInfo(startTime, endTime, message):
    ''' Logs information about elapsedTime '''
    elapsedTime = endTime - startTime
    logElapsedTime(elapsedTime, message)



def get_images(query):
	image_type="Action"
	query= query.split()
	query='+'.join(query)
	url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	print url
	#add the directory for your image here
	DIR="./results"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header)
	ActualImages=[]# contains the link for Large original images, type of  image
	for a in soup.find_all("div",{"class":"rg_meta"}):
	    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
	    ActualImages.append((link,Type))

	print  "there are total" , len(ActualImages),"images"
	if not os.path.exists(DIR):
		    os.mkdir(DIR)
	DIR = os.path.join(DIR, query.split()[0])
	if not os.path.exists(DIR):
		    os.mkdir(DIR)
	###print images
	counter = 0
	for i , (img , Type) in enumerate( ActualImages):
	    if counter > 0 :
		break
	    try:
		req = urllib2.Request(img, headers={'User-Agent' : header})
		raw_img = urllib2.urlopen(req).read()

		cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
		print cntr
		if len(Type)==0:
		    #f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
            f = open(os.path.join(DIR , "result.jpg"), 'wb')
		else :
		    #f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')
            f = open(os.path.join(DIR , "result.jpg"), 'wb')


		f.write(raw_img)
		f.close()
		counter = counter + 1
	    except Exception as e:
		print "could not load : "+img
		print e


def load_cnn():
	model = InceptionV3(weights='imagenet')
	return model

def cnn_predict(folder):
        class_results = []
        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        for im in onlyfiles:
		ext = im.split('.')[1]
		if ext == 'jpg':
			im_path = folder + '/' + im
			img = image.load_img(im_path,target_size=(299,299))
			x = image.img_to_array(img)
			x = np.expand_dims(x, axis=0)
			x = preprocess_input(x)
			preds = model.predict(x)
			# decode the results into a list of tuples (class, description, probability)
			# (one such list for each sample in the batch)
			res = decode_predictions(preds, top=3)[0][0][1]
			try:
				label = res.split('_')[1]
			except:
				label = res
			class_results.append(label)
	return class_results

def load_w2v():
	w2v_model = Word2Vec.load("wiki_model/wiki.en.word2vec.model")
	return w2v_model

def w2v_predict(words):
	w2v_input = ' '.join(words)
        answer = w2v_model.doesnt_match(w2v_input.split())
	return answer

if __name__ == "__main__":
	logging.basicConfig(filename='output.log', level=logging.DEBUG)
	startTime = datetime.datetime.now()
	model = load_cnn()
	loadCnnTime = datetime.datetime.now()
	logTimeInfo(startTime,loadCnnTime,"loadCnnTime")
	results = cnn_predict(IMAGE_DIR)
	predictCnnTime = datetime.datetime.now()
	logTimeInfo(loadCnnTime,predictCnnTime,"predictCnnTime")
	w2v_model = load_w2v()
	loadW2vTime = datetime.datetime.now()
	logTimeInfo(predictCnnTime,loadW2vTime,"loadW2vTime")
	query = w2v_predict(results)
	predictW2vTime = datetime.datetime.now()
	logTimeInfo(loadW2vTime,predictW2vTime,"predictW2vTime")
	get_images(query)
