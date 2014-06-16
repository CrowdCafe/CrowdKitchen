# TODO - needs to be rewritten
import requests 
from models import Job, DataUnit, Answer
from django.conf import settings

import re
import csv
import urllib2
import StringIO

def getGithubRepositoryFiles(extention):
	repository = settings.GITHUB_HTML_TEMPLATES['repository']
	owner = settings.GITHUB_HTML_TEMPLATES['owner']

	url = 'https://api.github.com/repos/'+owner+'/'+repository+'/contents'
	headers = {'User-Agent': owner}

	r = requests.get(url, headers = headers)
	
	prefix = 'https://raw.githubusercontent.com/'+owner+'/'+repository+'/master/'
	files = {}

	for f in r.json():
		if extention in f['path']:
			files[f['path']] = prefix+f['path']


	return [(v, k) for k, v in files.iteritems()]

def saveDataItems(job,dataset):
	if len(dataset)>0:
		for item in dataset:
			dataitem = DataItem(job = job, value = item)
			if 'gold' in item:
				if item['gold'] == '1' or item['gold'] == 1:
					print 'gold'
					print item
					dataitem.gold = True
			dataitem.save()


def collectDataFromSocialNetwork(keyword, amount, socialnetwork):
	if socialnetwork == 0: # Twitter
		return collectDataFromTwitter(keyword, amount)
	if socialnetwork == 1: # Instagram
		return 

def collectDataFromTwitter(keyword, amount):
	instance = UserSocialAuth.objects.filter(provider='twitter')[0]

	TWITTER_ACCESS_TOKEN = (instance.tokens).get('oauth_token')
	TWITTER_ACCESS_TOKEN_SECRET = (instance.tokens).get('oauth_token_secret')
	
	apicall=TwitterCall(client_id=TWITTER_ACCESS_TOKEN,client_secret=TWITTER_ACCESS_TOKEN_SECRET)
	
	dataset = apicall.getByKeyword(keyword, amount, False)
	return dataset

def simplifyInstagramDataset(dataset):
	simplified = []
	for item in dataset:
		if item['type']!='video':
			simplified.append({
			'id':item['id'],
			'link':item['link'],
			'image_url':item['images']['low_resolution']['url']
			})
	return simplified
def collectDataFromInstagram(keyword, amount):


	apicall = InstagramCall(settings.INSTAGRAM_CLIENT_ID, settings.INSTAGRAM_SECRET)
	dataset = apicall.getByKeyword(keyword, amount)

	return dataset