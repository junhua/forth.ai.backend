from django.conf import settings
from rest_framework.views import APIView
import requests, json

class Facebook():
	def __init__(self):
		self.__user_post_api = settings.FB_HOST + '/me/feed'
		self.__page_post_api = settings.FB_HOST + '/%s/feed'

		self.__me_base_api = settings.FB_HOST + '/me'
		self.__pages_api = settings.FB_HOST + '/me/accounts'
		self.__headers = {'Content-Type': 'application/json'}

	def get_me(self, access):
		me = {}
		me['provider'] = 'facebook'
		me['type'] = 0

		url = self.__me_base_api + '?fields=id,name,picture&access_token=%s' % access
		response = requests.get(url, headers = self.__headers)
		response = json.loads(response.content)

		me['uid'] = response['id']
		me['name'] = response['name']
		me['avatar'] = response['picture']['data']['url']

		return me

	def get_pages(self, access):
		pages = []

		url = self.__pages_api + '?access_token=%s' % access
		print 'page api is==============', url
		response = requests.get(url, headers = self.__headers)
		response = json.loads(response.content)['data'][0]
		print '??????????????   page respnse', response
		page = {}
		if response:
			for data in response:
				print'1111111================ data ==========', data 
				page['provider'] = 'facebook'
				page['type'] = 1
				page['uid'] = data['id']
				page['name'] = data['name']
				page['avatar'] = data['picture']['data']['url']

			pages.append(page)
		else:
			return None

		return pages

	def user_post(self, access, message):
		params = {
			'message': message,
			'access_token': access 
		}
		requests.post(self.__user_post_api, params = params)

	def page_access(self, page_id, access):
		page_access_api = settings.FB_HOST + '/%s/access_token' % page_id
		params = {
			'access_token': access
		}
		response = requests.post(page_access_api, params = params)

		page_access = json.loads(response.content)['access_token']
		return page_access

	def page_post(self, page_id, access, message):
		page_access = self.page_access(page_id, access)
		params = {
			'access_token': page_access
		}

		url = self.__page_post_api % page_id
		requests.post(url, params = params)
