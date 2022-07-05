#middleware需在setting中配置
import uuid

from django.utils.deprecation import MiddlewareMixin

USER_KEY='uid'
TEN_YEARS=60*60*24*365*10

class UserIDMiddleware(MiddlewareMixin):
	def __int__(self,get_response):
		self.get_response=get_response

	def __call__(self,request):
		#生成uid
		uid=self.generate_uid(request)
		request.uid=uid
		response=self.get_response(request)
		#设置cookie
		response.set_cookie(USER_KEY,uid,max_age=TEN_YEARS,httponly=True)
		return response

	def generate_uid(self,request):
		try:
			uid=request.COOKIES[USER_KEY]
		except KeyError:
			#首次生成随机串，hex消除"-"
			uid=uuid.uuid4().hex
		return uid