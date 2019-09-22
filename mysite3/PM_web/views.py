from PM_web.forms import UserForm,ProfileForm,CustomUserCreationForm,CustomUserEditForm
import datetime
from django.shortcuts import render, get_object_or_404,redirect,reverse,HttpResponseRedirect,HttpResponse
from PM_web.models import Profile,Team_information,Operator,station_info
from django.contrib.auth.models import User,Group
from django.contrib import messages 
from PM_web.forms import GroupForm ,Team_infoForm
from django.views import generic
from .tables import UserTable,GroupTable,OperatorTable
from django_tables2 import RequestConfig
from django.core.paginator import Paginator
from .filters import UserFilter,GroupFilter,OperatorFilter
from hashlib import sha1
from .forms import CustomUserCreationForm,CustomGroupCreationForm,CustomGroupEditForm
from django.views.generic import CreateView,UpdateView
def index(request):
    return render(request,'base_generic2.html')

# Create your views here.
def update_profile(request,pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            main_form=user_form.save()
            additional_form=profile_form.save(False)
            additional_form.user = main_form
            additional_form.save()
            #messages.success(request, _('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('search'))
        else:
                return render(request, 'PM_web/profile.html', {
                    'user_form': user_form,
                    'profile_form': profile_form
                })
            #messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
    return render(request, 'PM_web/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

 
#...
def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse('search'))
        else:
            return render(request, 'PM_web/register.html', {'form': f})
 
    else:
        f = CustomUserCreationForm()
        return render(request, 'PM_web/register.html', {'form': f})

def group_register(request):
    if request.method == 'POST':
        f = CustomGroupCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(reverse('search_group'))
        else:
            print(request.POST)
            print("form is invalid")
    else:
        f = CustomGroupCreationForm()
        #print(f)
    return render(request, 'PM_web/group_register.html', {'my_form': f})


#def update_team(request):
#    if request.method == "POST":
#        group_form= GroupForm(request.POST,instance=request.group)
#        team_form= Team_infoForm(request.POST,instance=request.group.team_information)
#        if group_form.is_valid() and team_form.is_valid():
#            group_form.save()
#            team_form.save()
#            messages.success(request, 'Group created successfully')
#        else:
#            messages.error(request, _('Please correct the error below.'))
#    else:
#        group_form = GroupForm()
#        team_form= Team_infoForm()
#    return render(request,'PM_web/group_reg.html',{
#        'group_form': group_form,
#        'team_form': team_form,
#        })
class UserListView(generic.ListView):
    model = User
    template_name="PM_web/user_list.html"

def people(request):
    #print("hello world!!!!!!!!!!!!!!!!")
    #print(User.objects.get(id=1).id)
    user_list=User.objects.all()
    page=request.GET.get('page',1)
    #paginator = Paginator(user_list,10)
    #try:
    #    users = paginator.page(page)
    #except PageNotAnInteger:
    #    users = paginator.page(1)
    #except EmptyPage:
    #    users=paginator.page(paginator.num_pages)
    table = UserTable(user_list)
    #RequestConfig(request).configure(table)
    RequestConfig(request,paginate={'per_page':10,'page':page}).configure(table)
    return render(request,'PM_web/people_list.html',{ 'users':table })
    #return render(request,'PM_web/my_table.html',{ 'table':table })




def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'PM_web/filter_test.html', {'filter': user_filter})

def search_user(request):
    user_list = User.objects.all()
    #page=request.GET.get('page',1)
    user_filter = UserFilter(request.GET, queryset=user_list)
    table = UserTable(user_filter.qs)
    RequestConfig(request,paginate={'per_page':10,'page':1}).configure(table)
    return render(request, 'PM_web/filter_test2.html', {'table':table,'filter': user_filter}) 

def search_group(request):
    groups_list = Group.objects.all()
    #print(request.GET)
    group_filter = GroupFilter(request.GET,queryset=groups_list)
    table = GroupTable(group_filter.qs)
    RequestConfig(request,paginate={'per_page':10,'page':1}).configure(table)
    return render(request, 'PM_web/filter_group.html', {'table':table,'filter': group_filter})


def user_details(request,pk):
    user = User.objects.get(id=pk)
    print("username: ",user)
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        #if f.is_valid():
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.set_password(request.POST['password1'])
        user.save()
        user.profile.phone = request.POST['phone']
        user.profile.save()
        #user.cleaned_data['team'].user_set.add(user)
        if(len(user.groups.all())==0):
            Group.objects.get(id=int(request.POST['team'])).user_set.add(user)
        elif(user.groups.all()[0] == request.POST['team']):
            user.groups.clear()
            Group.objects.get(id=int(request.POST['team'])).user_set.add(user)
        #messages.success(request, 'Account created successfully')
        return HttpResponseRedirect(reverse('search'))
    else:
        print("alowha!!!")
        
        #form = CustomUserCreationForm(initial={'username':user.username,'email':user.email,'password1':user.password,'password2':user.password,'phone':user.profile.phone,'team':user.groups } )
        if(len(user.groups.all())==0):
            form = CustomUserCreationForm(initial={'username':user.username,'email':user.email,'phone':user.profile.phone} )
        else:
            form = CustomUserCreationForm(initial={'username':user.username,'email':user.email,'phone':user.profile.phone,'team':user.groups.all()[0] } )
        return render(request, 'PM_web/register.html', {'form': form})

def update_user_info(request,pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        f = CustomUserEditForm(request.POST,user_id=pk)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(reverse('search'))
        else:
            return render(request, 'PM_web/register.html', {'form': f})
    else:
        if(len(user.groups.all())==0):
            form = CustomUserEditForm(initial={'username':user.username,'email':user.email,'phone':user.profile.phone},user_id=pk )
        else:
            form = CustomUserEditForm(initial={'username':user.username,'email':user.email,'phone':user.profile.phone,'team':user.groups.all()[0] },user_id=pk )
        return render(request, 'PM_web/register.html', {'form': form})
def update_group_info(request,pk):
    team = Group.objects.get(id=pk)
    print("team: ",team)
    #if request.POST.get('Delete'):
    #    print("delete!!!!!")
    if request.method == 'POST':
        #print(request.POST)
        f = CustomGroupEditForm(request.POST,teamid=pk)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(reverse('search_group'))
        else:
            print("invalid data")
            return render(request,'PM_web/group_register.html', {'my_form': f})
    else:
        form = CustomGroupEditForm(initial={'name':team.name,'type':team.team_information.type,'manager':team.team_information.manager,'create_time':team.team_information.create_time.strftime('%Y-%m-%d %H:%M:%S')},teamid=pk)
        return render(request,'PM_web/group_editing.html', {'my_form': form})
#def delete_group(request,pk):
#    Group.objects.filter(id=pk).delete()
#    return HttpResponseRedirect(reverse('search_group'))
def delete_group(request,pk):
    if request.method == "POST":
        # 找不到不处理
        #print("pk: ",pk)
        try:
            team = Group.objects.get(id=pk)
        except:
            return HttpResponse(status=404)
        data = request.POST
        method = data.get('_method', '').lower()
        if method == 'delete':
            team.delete()
            #print("request: ",request)
            return redirect('search_group')
def delete_user(request,pk):
    if request.method == "POST":
        # 找不到不处理
        #print("pk: ",pk)
        try:
            member = User.objects.get(id=pk)
        except:
            return HttpResponse(status=404)
        data = request.POST
        method = data.get('_method', '').lower()
        if method == 'delete':
            member.delete()
            #print("request: ",request)
            return redirect('search')
def delete_operator(request,pk):
    if request.method == "POST":
        # 找不到不处理
        #print("pk: ",pk)
        try:
            member = Operator.objects.get(id=pk)
        except:
            return HttpResponse(status=404)
        data = request.POST
        method = data.get('_method', '').lower()
        if method == 'delete':
            member.delete()
            #print("request: ",request)
            return redirect('search_operator')

class OperatorCreateView(CreateView):
    model = Operator
    fields = "__all__"
    template_name = "PM_web/operator_new.html"
    def get_success_url(self):
        return reverse('search_operator')
class OperatorUpdateView(UpdateView):
    model = Operator
    fields = "__all__"
    template_name = "PM_web/operator_edit.html"

def search_operator(request):
    f = OperatorFilter(request.GET,queryset=Operator.objects.all())
    table= OperatorTable(f.qs)
    RequestConfig(request,paginate={'per_page':10,'page':1}).configure(table)
    return render(request,'PM_web/search_operator.html',{'filter':f,'table':table})
