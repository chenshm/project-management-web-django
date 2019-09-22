from django import forms
from django.contrib.auth.models import User, Group
from PM_web.models import Profile,Team_information,Operator,station_info
import django_filters
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    year_joined = django_filters.NumberFilter(field_name='date_joined', lookup_expr='year')
    #groups = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(),
    #    widget=forms.CheckboxSelectMultiple)
    groups = django_filters.ModelChoiceFilter(queryset=Group.objects.all())
    profile__phone = django_filters.CharFilter(label='phone',lookup_expr= 'iexact' )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'year_joined', 'groups']


choice= (('1','研发团队'),('2','测试团队'),('3','项目团队'),('4','产品团队'),('5','架构团队'),('6','售前团队'),('7','驻地团队'),('8','运管团队'),('9','运维团队'),('0','其他团队'),)


class GroupFilter(django_filters.FilterSet):
    team_information__type = django_filters.ChoiceFilter(label='团队类型',choices=choice)
    team_information__manager = django_filters.ModelChoiceFilter(label='manager',queryset=User.objects.all())
    team_information_time_gt = django_filters.DateTimeFilter(label='搜索起始日期 format: Y-m-d H:M:S  ',field_name='team_information__create_time', lookup_expr='gte',input_formats=["%d/%m/%Y %H:%M"])
    team_information_time_lt = django_filters.DateTimeFilter(label='搜索截止日期 format: Y-m-d H:M:S  ',field_name='team_information__create_time', lookup_expr='lte',input_formats=["%d/%m/%Y %H:%M"])
    #i=DateTimePicker(options={'userCurrent':True,'collapse': False},attrs={'append':'fa fa-calendar','icon_toggle': True})
    #i=DatePicker()
    #team_information_time_gt = django_filters.DateTimeFilter(label='搜索起始日期',field_name='team_information__create_time', lookup_expr='gte',widget =i,)
    #team_information_time_lt = django_filters.DateTimeFilter(label='搜索截止日期',field_name='team_information__create_time', lookup_expr='lte',widget =i,)
    class Meta:
        model = Group
        fields = ['name']

class OperatorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Operator
        fields = "__all__"

