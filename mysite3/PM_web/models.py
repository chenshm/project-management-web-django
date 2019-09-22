from django.db import models
#-*-coding: utf-8 -*-
# Create your models here.
from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12,blank=True)
    #user_id = models.CharField(max_length=12)
    #staff_id = models.CharField(max_length=20,blank=True)
    #create_time = models.DateTimeField(default=timezone.now)
    #team = models.ForeignKey('Team_info', on_delete=models.CASCADE, default='1')
    def __str__(self):
        return self.user.username
    #this save method is used to avoid creating the same profile twice when creating user and profile inline at the same time
    def save(self, *args, **kwargs): 
        if not self.pk:
            try:
                p = Profile.objects.get(user=self.user)
                self.pk = p.pk
            except Profile.DoesNotExist:
                pass
        super(Profile,self).save(*args,**kwargs)
#    class Meta:
#        unique_together = (("user","phone"))
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Team_information(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    choice= (('1','研发团队'),('2','测试团队'),('3','项目团队'),('4','产品团队'),('5','架构团队'),('6','售前团队'),('7','驻地团队'),('8','运管团队'),('9','运维团队'),('0','其他团队'))
    type = models.CharField(max_length=32, choices=choice, default='3')
    manager = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group.name
    def save(self,*args,**kwargs):
        if not self.pk:
            try:
                t = Team_information.objects.get(group=self.group)
                self.pk = t.pk
            except Team_information.DoesNotExist:
                pass
        super(Team_information,self).save(*args,**kwargs)


@receiver(post_save, sender=Group)
def create_group_detail(sender, instance, created, **kwargs):
    if created:
        Team_information.objects.create(group=instance)

@receiver(post_save, sender=User)
def save_group_detail(sender, instance, **kwargs):
    instance.profile.save()



class Operator(models.Model):
    province_choice=(
        ('京','北京市'),
        ('津','天津市'),
        ('冀','河北省'),
        ('晋','山西省'),
        ('内蒙古','内蒙古自治区'),
        ('辽','辽宁省'),
        ('吉','吉林省'),
        ('黑','黑龙江省'),
        ('沪','上海市'),
        ('苏','江苏省'),
        ('浙','浙江省'),
        ('皖','安徽省'),
        ('闽','福建省'),
        ('赣','江西省'),
        ('鲁','山东省'),
        ('豫','河南省'),
        ('鄂','湖北省'),
        ('湘','湖南省'),
        ('粤','广东省'),
        ('桂','广西壮族自治区'),
        ('琼','海南省'),
        ('川','四川省'),
        ('贵','贵州省'),
        ('滇','云南省'),
        ('渝','重庆市'),
        ('藏','西藏自治区'),
        ('陕','陕西省'),
        ('甘','甘肃省'),
        ('青','青海省'),
        ('宁','宁夏回族自治区'),
        ('新','新疆维吾尔自治区'),
        ('港','香港特别行政区'),
        ('澳','澳门特别行政区'),
        ('台','台湾省'), )
    province = models.CharField('运营商所属省份',max_length=32, blank=False,choices=province_choice,default='沪')
    city = models.CharField(max_length=32, default='')
    name = models.CharField(max_length=32)
    choice = (('1','第一优先级'),('2','第二优先级'),('3','第三优先级'))
    priority = models.CharField(max_length=12, choices=choice, default=2)
    total_user = models.IntegerField(default=0)
    total_boot_user = models.IntegerField(default=0)
    total_incoming = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class station_info(models.Model):
    station_id = models.CharField(max_length=20, blank=False,help_text="驻地id")
    station_name = models.CharField(max_length=52, blank=False,help_text="驻地名称")
    station_manager = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,help_text="驻地总经理")
    #station_principal = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,help_text="驻地负责人")
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)






