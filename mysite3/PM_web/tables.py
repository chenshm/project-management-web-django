import django_tables2 as tables
import string
from django.contrib.auth.models import User,Group
from PM_web.models import Profile,Team_information,Operator,station_info
from django_tables2.utils import A
class UserTable(tables.Table):
	#id = tables.Column(accessor='user.id')
	username = tables.LinkColumn('user_detail',args=[A('pk')])
	#email = tables.Column(accessor='user.email')
	groups = tables.Column(empty_values=())	
	phone = tables.Column(empty_values=())
	delete = tables.TemplateColumn(
	'<form action="/PM_web/delete_user/{{record.id}}" method="post">{% csrf_token %}<input type="hidden" name="_method" value="delete"><button data-toggle="tooltip" title="Please note that deletion cannot be undone" type="submit" class="btn btn-danger btn-xs">delete</button></form>',
	orderable=False,
	verbose_name='',
	)
	class Meta:
		model = User
		template_name = 'django_tables2/bootstrap.html'
		fields = ('id','username','email','phone','groups')
	def render_groups(self,record):
		if record.groups.all():
			return ', '.join([group.name for group in record.groups.all() ])
		return '-'
	def render_phone(self,record):
		if record.profile.phone:
			return ', '.join([record.profile.phone ])
		return '-'
class GroupTable(tables.Table):
	name = tables.LinkColumn('team_update',args=[A('pk')])
	types = tables.Column(empty_values=())
	manager = tables.Column(empty_values=())
	createtime = tables.Column(empty_values=())
	#delete = tables.LinkColumn('delete_group',args=[A('pk')],attrs={'a':{'class':'btn btn-danger'}})
	delete = tables.TemplateColumn(
        '<form action="/PM_web/delete_group/{{record.id}}" method="post">{% csrf_token %}<input type="hidden" name="_method" value="delete"><button data-toggle="tooltip" title="Please note that deletion cannot be undone" type="submit" class="btn btn-danger btn-xs">delete</button></form>',
        orderable=False,
        verbose_name='',

    )
	class Meta:
		model = Group
		template_name = 'django_tables2/bootstrap.html'
		fields = ('name',)
	def render_types(self,record):
		choice= {'1':'研发团队','2':'测试团队','3':'项目团队','4':'产品团队','5':'架构团队','6':'售前团队','7':'驻地团队','8':'运管团队','9':'运维团队','0':'其他团队'}
		if record.team_information.type:
			return ', '.join([choice[record.team_information.type]])
		return '-'
	def render_manager(self,record):
		if record.team_information.manager:
			return ', '.join([record.team_information.manager.username])
		return '-'
	def render_createtime(self,record):
		if record.team_information.create_time:
			return ', '.join([record.team_information.create_time.strftime("%d/%m/%Y %H:%M")])
		return '-'
class OperatorTable(tables.Table):
	delete = tables.TemplateColumn(
	'<form action="/PM_web/delete_operator/{{record.id}}" method="post">{% csrf_token %}<input type="hidden" name="_method" value="delete"><button data-toggle="tooltip" title="Please note that deletion cannot be undone" type="submit" class="btn btn-danger btn-xs">delete</button></form>',
	orderable=False,
	verbose_name='',
	)
	name = tables.LinkColumn('update_operator',args=[A('pk')])
	class Meta:
		model = Operator
		template_name = 'django_tables2/bootstrap.html'
		#fields = "__all__"