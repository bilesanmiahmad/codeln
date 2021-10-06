from django.contrib import admin
from chatapp.models import ChannelMembership, Channel, ChannelMessage
# Register your models here.
admin.site.register(Channel)
admin.site.register(ChannelMessage)
admin.site.register(ChannelMembership)
