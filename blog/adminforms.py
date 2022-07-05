#定义管理员页面表单，取代adminmodel默认表单
from django import forms

class PostAdminForm(forms.ModelForm):
	desc = forms.CharField(widget=forms.Textarea,label='摘要',required=False)
