from django.db import models
from django.contrib.auth.models import User

from django.utils.functional import cached_property
import mistune

# Create your models here.
class Category(models.Model):
	STATUS_NORMAL = 1
	STATUS_DELETE = 0
	STATUS_ITEMS = (
		(STATUS_NORMAL,'正常'),
		(STATUS_DELETE,'剔除'),
	)

	name = models.CharField(max_length=50,verbose_name='名称')
	status = models.PositiveIntegerField(default=STATUS_NORMAL,
		choices=STATUS_ITEMS,verbose_name='状态')
	is_nav = models.BooleanField(default=False,verbose_name='是否为导航')
	owner = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	class Meta:
		verbose_name = verbose_name_plural = '分类'

	def __str__(self):
		return self.name

	@classmethod
	def get_navs(cls):
		categories = cls.objects.filter(status=cls.STATUS_NORMAL)
		'''
		nav_categories = categories.filter(is_nav=True)
		normal_categories = categories.filter(is_nav=False)
		#不管添加多少filter，只有filter返回queryset对象被使用（除调用filter外）时才进行数据库查询
		#此处调用nav_categorie等两个queryset对象，进行两次查询
		return {
			'navs':nav_categories,
			'categories':normal_categories
		}
		'''
		#只进行一次查询
		nav_categories = []
		normal_categories = []
		for cate in categories:
			if cate.is_nav:
				nav_categories.append(cate)
			else:
				normal_categories.append(cate)

		return {
			'navs':nav_categories,
			'categories':normal_categories
		}

class Tag(models.Model):

	STATUS_NORMAL = 1
	STATUS_DELETE = 0
	STATUS_ITEMS = (
		(STATUS_NORMAL,'正常'),
		(STATUS_DELETE,'删除'),
	)

	name = models.CharField(max_length=10,verbose_name='名称')
	status = models.PositiveIntegerField(default=STATUS_NORMAL,
		choices=STATUS_ITEMS,verbose_name='状态')
	owner = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	class Meta:
		verbose_name = verbose_name_plural = '标签'

	#配置页面展示名称
	def __str__(self):
		return self.name
	
class Post(models.Model):
	def __str__(self):
		return self.name
	
	STATUS_NORMAL = 1
	STATUS_DELETE = 0
	STATUS_DRAFT = 2
	STATUS_ITEMS = (
		(STATUS_NORMAL,'正常'),
		(STATUS_DELETE,'删除'),
		(STATUS_DRAFT,'草稿'),
	)

	title = models.CharField(max_length=255,verbose_name='标题')
	desc = models.CharField(max_length=1024,blank=True,verbose_name='摘要')
	content = models.TextField(verbose_name='正文',help_text='必须为MarkDown')
	content_html = models.TextField(verbose_name='正文html代码', blank=True,editable=False)
	status = models.PositiveIntegerField(default=STATUS_NORMAL,
		choices=STATUS_ITEMS,verbose_name='状态')
	#django3必须加on_delete参数
	category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
	tag = models.ManyToManyField(Tag,verbose_name='标签')
	owner = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	#访问量
	pv = models.PositiveIntegerField(default=1)
	uv = models.PositiveIntegerField(default=1)

	class Meta:
		verbose_name = verbose_name_plural = '文章'
		#降序排列
		ordering = ['-id']

	def __str__(self):
		return self.title

	#静态方法，没有self、cls参数，不能获得类中定义属性&方法，只能用类名调用
	@staticmethod
	def get_by_tag(tag_id):
		try:
			#objects是Manager类型的对象，Tag.objects=Models.Manager()
			tag = Tag.objects.get(id=tag_id)
		#object.DoesNotExist
		except Tag.DoesNotExist:
			tag = None
			post_list = []
		else:
			#post_set来自objects.get，此方法返回符合条件的对象集合
			#tag是post的外键，外键查询时需要返回model的小写（此处为'post')+'_set'
			#select_related先使用innerjoin连接post和tag，进行一次数据库查询
			#不使用select_related，先查询tag，获得tag_id对应Tag对象，再在post中查找tag字段为Tag对象的Post，需要两次查找
			post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
				.select_related('owner','category')

		return post_list,tag

	@staticmethod
	def get_by_category(category_id):
		try:
			category = Category.objects.get(id=category_id)
		except:
			category = None
			post_list = []
		else:
			post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
				.select_related('owner','category')

		return post_list, category

	@classmethod
	#类方法，有cls参数，传入类，可通过类名/对象名调用
	def latest_posts(cls):
		queryset = cls.objects.filter(status=cls.STATUS_NORMAL)

		return queryset
	
	@classmethod
	def hot_posts(cls):
		#按pv降序
		return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')[:3]

	def save(self,*args,**kwargs):
		self.content_html = mistune.markdown(self.content)
		super().save(*args,*kwargs)

	@cached_property
	def tags(self):
		return ','.join(self.tag.values_list('name',flat=True))