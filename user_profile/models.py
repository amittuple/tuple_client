from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username


class InviteMail(models.Model):
    uuid = models.CharField(max_length=200, null=False, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    receiver = models.CharField(max_length=200)
    sender = models.ForeignKey(User)
    registered = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Invite Mail To : %s' % self.receiver


class CompanyDetail(models.Model):
    admin = models.OneToOneField(User)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    max_members = models.IntegerField(default=5)

    def __unicode__(self):
        return u'Company Details By : %s' % self.admin

class ServerDetails(models.Model):
    user = models.OneToOneField(User)
    task_id = models.CharField(max_length=200, null=True, blank=True)
    instance_id = models.CharField(max_length=200, null=True, blank=True)
    hosted_zone_id = models.CharField(max_length=200, null=True, blank=True)
    subdomain = models.CharField(max_length=200, null=True, blank=True)
    server_status = models.CharField(max_length=200, null=True, blank=True)
    name_server_list = models.CharField(max_length=200, null=True, blank=True)
    ip_address = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return u'Server Details Of User: %s' % self.user.username


class MembersList(models.Model):
    member = models.OneToOneField(User)
    company_id = models.ForeignKey(CompanyDetail)
    is_admin = models.BooleanField(default=True)
    server = models.ForeignKey(ServerDetails)

    def __unicode__(self):
        return u'Member : %s' % self.member



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)
        server, new = ServerDetails.objects.get_or_create(user=instance)
        company, new = CompanyDetail.objects.get_or_create(admin=instance)
        member, new = MembersList.objects.get_or_create(member=instance, company_id=company)





