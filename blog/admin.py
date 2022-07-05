from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post,Category,Tag
from django.contrib.admin.models import LogEntry

#使用自定义表单
from .adminforms import PostAdminForm

from myblog.base_admin import BaseOwnerAdmin
from myblog.custom_site import custom_site

#关联模型
class PostInline(admin.TabularInline):
	fields = ('title','desc')
	extra = 1
	model = Post

# Register your models here.
@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
	#关联Category&Post，将在Categrory页面新增Post编辑链接
	inlines = [PostInline,]

	list_display = ('name','status','is_nav','created_time','post_count')
	fields = ('name','status','is_nav')

	def post_count(self,obj):
		return obj.post_set.count()

	post_count.short_description = '文章数量'
	
@admin.register(Tag,site=custom_site)
#继承modeladmin
class TagAdmin(BaseOwnerAdmin):
	list_display = ('name','status','created_time')
	fields = ('name','status')

#定义category过滤器，使用list_filter指定按category过滤即可使用此过滤器
class CategoryOwnerFilter(admin.SimpleListFilter):
	title = '分类过滤器'
	#查询url参数为owner_category
	parameter_name = 'owner_category'

	#返回展示过滤条件列表，这里展示Category_name
	def lookups(self,request,model_admin):
		return Category.object.filter(owner=request.user).values_list('id','name')

	#参数为queryset文章组合列表
	def queryset(self,request,queryset):
		category_id = self.value()
		if category_id:
			#使用queryset的filter方法过滤，过滤结果为另一个queryset，self.value有lookups选定
			return queryset.filter(category_id=self.value())
		return queryset
	
#使用自定义site
@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
	#使用自定义表单
	form = PostAdminForm
	#成功加入数据后列表展示那些字段
	list_display = [
		'title','category','status',
		'created_time','operator','owner'
	]
	#哪些字段可以作为链接
	list_display_links = []
	#根据哪些字段过滤数据展示列表
	list_filter = ['category',]
	#配置搜索字段，双下划线引用属性name
	search_fields = ['title','category__name']

	#动作相关配置是否展示在顶部
	action_on_top = True
	#动作相关配置是否展示在底部
	action_on_bottom = True
	#保存、编辑、编辑并新建按钮是否在顶部展示
	save_on_top = True

	'''
	#要展示的字段&顺序
	fields = (
		('category','title'), #元组内元素放在同一个div
		'desc',
		'status',
		'content',
		'tag',
	)'''
	fieldsets = (
		#(名称，{内容})
		('基础配置',{
			'description':'基础配置描述',
			'fields':(
				('title','category'),
				'status',
			),
		}),
		('内容',{
			'fields':(
				'desc',
				'content',
			),
		}),
		('额外信息',{
			#classes定义CSS属性
			'classes':('collapse',),
			'fields':('tag',),
		})
	)

	filter_horizontal = ('tag',)


	def operator(self,obj):
		#{}内填充为reverse返回路由
		return format_html(
			'<a href="{}">编辑</a>',
			#使用admin配置的路由admin/app名称/model名称/ID值/change/，id取obj.id
			#重定向到admin/app名称/model名称/ID值/change/
			#reverse('admin:blog_post_change',args=(obj.id,))
			reverse('cus_admin:blog_post_change',args=(obj.id,))
		)
	operator.short_description = '操作'

	#使用自定义CSS&js，不确定内容是谨慎使用，如可能覆盖admin的collapse的CSS属性，造成显示错误
	'''class Media:
		css = {
			'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
		}
		js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)
	'''


@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
	list_display = ['object_repr','object_id','action_flag','user','change_message']

