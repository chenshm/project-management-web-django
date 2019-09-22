import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm
from PM_web.models import Profile,Team_information
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from bootstrap_datepicker_plus import DatePickerInput,DateTimePickerInput
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username' ,'first_name', 'last_name', 'email','password',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone',)


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User ,Group
from django import forms
from django.core.exceptions import ValidationError
from PM_web.models import Profile, Team_information
 
class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    phone = forms.CharField(max_length=12)
    team = forms.ModelChoiceField(queryset=Group.objects.all(),required=False)
 
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username
 
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        r = Profile.objects.filter(phone=phone)
        if r.count():
            raise  ValidationError("phone already exists")
        return phone


    def save(self, commit=True):
        u = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        u.profile.phone = self.cleaned_data['phone']
        u.save()
        print(type(self.cleaned_data['team']))
        if self.cleaned_data['team'] is None:
            pass
        else:
            self.cleaned_data['team'].user_set.add(u)
        return u
    #def edit_save(self, commit=True,user=user):
    #    user.username = self.cleaned_data['username']
    #    user.email = self.cleaned_data['email']
    #    user.password = self.cleaned_data['password1']
    #    user.save()
    #    user.profile.phone = self.cleaned_data['phone']
    #    user.cleaned_data['team'].user_set.add(user)
class CustomUserEditForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    phone = forms.CharField(max_length=12)
    team = forms.ModelChoiceField(queryset=Group.objects.all(),required=False)
    def __init__(self,*args,**kwargs):
        self.userid = kwargs.pop('user_id')
        super(CustomUserEditForm,self).__init__(*args,**kwargs)
    def clean_username(self):
        username = self.cleaned_data['username']
        if username and User.objects.filter(username=username).exclude(id=self.userid).count():
            raise forms.ValidationError("This username is already in use. Please use a different username")
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exclude(id=self.userid).count():
            raise forms.ValidationError("This email address is already in use. Please use a different email address")
        return email
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        r = Profile.objects.filter(phone=phone)
        if phone and (Profile.objects.filter(phone=phone).count()>1):
            raise  ValidationError("phone already exists")
        return phone
    def save(self, commit=True):
        user = User.objects.get(id=self.userid)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.save()
        user.profile.phone = self.cleaned_data['phone']
        user.profile.save()
        print("type: ",type(self.cleaned_data['team']))
        if(len(user.groups.all())==0):
            self.cleaned_data['team'].user_set.add(user)
        elif self.cleaned_data['team'] is None:
            user.groups.clear()
        elif(user.groups.all()[0] == self.cleaned_data['team']):
            user.groups.clear()
            self.cleaned_data['team'].user_set.add(user)
        return user
class CustomGroupCreationForm(forms.Form):
    name = forms.CharField(label='Enter Groupname', min_length=4, max_length=150)
    choice = (('1','研发团队'),('2','测试团队'),('3','项目团队'),('4','产品团队'),('5','架构团队'),('6','售前团队'),('7','驻地团队'),('8','运管团队'),('9','运维团队'),('0','其他团队'))
    type = forms.ChoiceField(choices=choice)
    manager = forms.ModelChoiceField(queryset=User.objects.all(),required=True )
    create_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M']
        )
    update_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M']
        )
    # warning!!!!!!!!!!!!!!!!!!!!!!!!!
    #create_time =  forms.DateTimeField(
    #    widget = DateTimePicker(
    #        options={
    #            'userCurrent':True,
    #            'collapse': False,
    #        },
    #        attrs={
    #            'append':'fa fa-calendar',
    #            'icon_toggle':True,
    #        }
    #    ),
    #)
    #update_time =  forms.DateTimeField(
    #    widget = DateTimePicker(
    #        options={
    #            'userCurrent':True,
    #            'collapse': False,
    #        },
    #        attrs={
    #            'append':'fa fa-calendar',
    #            'icon_toggle':True,
    #        }
    #    ),
    #)

    def clean_name(self):
        name = self.cleaned_data['name']
        r = Group.objects.filter(name=name)
        if r.count():
            raise  ValidationError("Groupname already exists")
        return name

    def save(self, commit=True):
        g = Group.objects.create(
            name=self.cleaned_data['name']
        )
        #print("type!!!!!!!!!!!!!!!!!!!!!: ",type(self.cleaned_data['type']))
        #print("manager++++++++++++++++++: ",type(self.cleaned_data['manager']))
        g.team_information.type =self.cleaned_data['type']
        g.team_information.manager = self.cleaned_data['manager']
        g.team_information.create_time = self.cleaned_data['create_time']
        g.team_information.update_time = self.cleaned_data['update_time']
        g.save()
        g.team_information.save()
        return g

class CustomGroupEditForm(forms.Form):
    name = forms.CharField(label='Enter Groupname', min_length=4, max_length=150)
    choice = (('1','研发团队'),('2','测试团队'),('3','项目团队'),('4','产品团队'),('5','架构团队'),('6','售前团队'),('7','驻地团队'),('8','运管团队'),('9','运维团队'),('0','其他团队'))
    type = forms.ChoiceField(choices=choice)
    manager = forms.ModelChoiceField(queryset=User.objects.all(),required=True )
    create_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M']
        )
    #create_time =  forms.DateTimeField(
    #    input_formats=['%d/%m/%Y %H:%M'],
    #    widget = DateTimePicker(
    #        options={
    #            'userCurrent':True,
    #            'collapse': False,
    #        },
    #        attrs={
    #            'append':'fa fa-calendar',
    #            'icon_toggle':True,
    #        }
    #    ),
    #)
    def __init__(self,*args,**kwargs):
        self.teamid = kwargs.pop('teamid')
        super(CustomGroupEditForm,self).__init__(*args,**kwargs)
    def clean_name(self):
        name = self.cleaned_data['name']
        if name and Group.objects.filter(name=name).exclude(id=self.teamid).count():
            raise forms.ValidationError("This username is already in use. Please use a different username")
        return name
    def save(self, commit=True):
        team = Group.objects.get(id=self.teamid)
        team.name = self.cleaned_data['name']
        team.save()
        team.team_information.type = self.cleaned_data['type']
        team.team_information.manager = self.cleaned_data['manager']
        team.team_information.create_time = self.cleaned_data['create_time']
        team.team_information.save()
        return team
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)

class Team_infoForm(forms.ModelForm):
    class Meta:
        model = Team_information
        fields = "__all__"