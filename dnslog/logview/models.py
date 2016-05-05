from django.db import models
from django.contrib import admin

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    udomain = models.CharField(max_length=128)
    def __unicode__(self):
        return self.username
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'udomain')

admin.site.register(User, UserAdmin)


class WebLog(models.Model):
    user = models.ForeignKey(User)
    path = models.TextField('path')
    remote_addr = models.GenericIPAddressField('remote_addr')
    http_user_agent = models.TextField('user_agent')
    log_time = models.DateTimeField('time loged', auto_now_add=True)

    def __unicode__(self):
        return self.remote_addr

    class Meta:
        ordering = ['log_time']
class WebLogAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'path', 'remote_addr', 'http_user_agent', 'log_time')

admin.site.register(WebLog, WebLogAdmin)


class DNSLog(models.Model):
    user = models.ForeignKey(User)
    host = models.TextField('host')
    type = models.TextField('dns type')
    log_time = models.DateTimeField('time loged', auto_now_add=True)

    def __unicode__(self):
        return self.host

    class Meta:
        ordering = ['log_time']

class DNSLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'host', 'type', 'log_time')

admin.site.register(DNSLog, DNSLogAdmin)
