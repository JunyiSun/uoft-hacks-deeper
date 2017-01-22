from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import imagenet_classification
import sys
import os
import datetime
import simplejson as json
import pdb
#-----
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
import logging
import datetime
import shutil
import subprocess
import re

IMAGE_DIR = '/Users/joeybose/Desktop/hackathon/images'

app = Flask(__name__)
api = Api(app)

IMAGES = {
    'input': './uploads',
    'output': 'output directory',
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in IMAGES:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


class Image(Resource):
	def __init__(self, model, w2v_model):
		print ' in constructor'
		self.model = model
		print 'assigned model'
		self.w2v_model = w2v_model
		print 'assigned w2v_model'

	def get(self, todo_id):
	    abort_if_todo_doesnt_exist(todo_id)
	    return IMAGES[todo_id]

	def delete(self, todo_id):
	    abort_if_todo_doesnt_exist(todo_id)
	    del IMAGES[todo_id]
	    return '', 204

	def put(self, todo_id):
		useless = {'task': 'results.jpg'}

		print "BeforeParseArgs"
		args = parser.parse_args()
		task = args['task']
		print task
		captions = self.get_captions(task)
		print captions
		#output = {'image1': captions[0], 'image2': captions[1], 'image3': captions[2]}
		#jsonOutput = json.dumps(output)
		#print jsonOutput
		listOutput = [captions[0], captions[1], captions[2]]
		#return listOutput
		results = self.cnn_predict(task, self.model)
		#results = self.cnn_predict(task, model)
		#results = self.cnn_predict(task, Image.model)
		print 'predicted'
		query = self.w2v_predict(results, self.w2v_model)
		#query = self.w2v_math(results, self.w2v_model)
		print 'predicted'
		self.get_images(query)
		print 'getted'
		IMAGES[todo_id] = query
		return listOutput
		#return output, 201

	def get_captions(self,folder):
		p = subprocess.Popen(["th", "/Users/joeybose/Desktop/hackathon/neuraltalk2/eval.lua", "-model", 
					"/Users/joeybose/Desktop/hackathon/neuraltalk2/model_cpu.t7",
					"-image_folder", folder, "-num_images", "3"], stdout=subprocess.PIPE)
		output, err = p.communicate()
		lines = output.splitlines()
		captions = []
		for line in lines:
			try:
				caption = line.split(':')
				if re.search(r'\d', caption[0]):
					result = caption[1].strip('\t')
					captions.append(result)
			except:
				haha = 0
		return captions

	def get_soup(self, url,header):
	    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

	def logElapsedTime(self, elapsedTime, message):
	    ''' Logs the elapsedTime with a given message '''
	    hours, remainder = divmod(elapsedTime.seconds, 3600)
	    minutes, seconds = divmod(remainder, 60)
	    totalDays = elapsedTime.days
	    print str(message) + ': Days: ' + str(totalDays) +  " hours: " + str(hours) + ' minutes: ' + str(minutes) +  ' seconds: ' + str(seconds)

	def logTimeInfo(self, startTime, endTime, message):
	    ''' Logs information about elapsedTime '''
	    elapsedTime = endTime - startTime
	    logElapsedTime(elapsedTime, message)

	def get_images(self, query):
		image_type="Action"
		print query
		query= query.split()
		query='+'.join(query)
		url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
		print url
		#add the directory for your image here
		DIR="./results"
		header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
		soup = self.get_soup(url,header)
		ActualImages=[]# contains the link for Large original images, type of  image
		for a in soup.find_all("div",{"class":"rg_meta"}):
		    link , Type = json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
		    ActualImages.append((link,Type))

		print  "there are total" , len(ActualImages),"images"
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
			f = open(os.path.join(DIR , "result.jpg"), 'wb')
			f.write(raw_img)
			f.close()
			counter = counter + 1
		    except Exception as e:
			print "could not load : "+img
			print e


	def load_cnn(self):
		model = InceptionV3(weights='imagenet')
		return model

	def cnn_predict(self, folder,model):
		class_results = []
		onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
		try:
			shutil.rmtree('results/')
		except:
			print('Failed to Delete Results')
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

	def load_w2v(self):
		w2v_model = Word2Vec.load("wiki_model/wiki.en.word2vec.model")
		return w2v_model

	def w2v_predict(self, words,w2v_model):
		w2v_input = ' '.join(words)
		answer = w2v_model.doesnt_match(w2v_input.split())
		return answer

	def w2v_math(self, words,w2v_model):
		print words
                answer = w2v_model.most_similar(positive=[words[0], words[1]], negative=[words[2]])[0][0]
                return answer


# ImageList
# shows a list of all IMAGES, and lets you POST to add new tasks
class ImageList(Resource):
    def get(self):        
        return IMAGES

class Home(Resource):
    def get(self):        
        return IMAGES


##
## Actually setup the Api resource routing here
##

if __name__ == '__main__':
	print 'begin loading model'
	my_model = InceptionV3(weights='imagenet')

	print 'begin loading 2nd model'
	my_w2v_model = Word2Vec.load("wiki_model/wiki.en.word2vec.model")
	print 'end loading models'
	api.add_resource(ImageList, '/images')
	#api.add_resource(Image, '/images/<todo_id>')
	print 'Adding model resources'
	api.add_resource(Image, '/images/<todo_id>', resource_class_kwargs={'model': my_model, 'w2v_model':my_w2v_model})
	api.add_resource(Home, '/')
	print "before run app"	
	app.run(debug=False)
	print "after run app"
