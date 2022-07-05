from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
	exclude = ('owner',)

	def get_queryset(self,request):
		qs = super(BaseOwnerAdmin,self).get_queryset(request)
		return qs.filter(owner=request.user)

	#重写save_model方法
	def save_model(self,request,obj,form,change):
		#owner字段非空，设置为当前用户
		obj.owner = request.user
		#super(TagAdmin,self) 首先找到 父类，然后把类 TagAdmin 的对象转换为父类的对象，并调用父类的save_model将obj存到数据库
		return super(BaseOwnerAdmin,self).save_model(request,obj,form,change)
