from django.contrib import admin
from supportapp.models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'date', 'status')
    search_fields = ('id', 'title', 'status')
    list_editable = ('status',)
    list_filter = ('status',)


admin.site.register(Ticket, TicketAdmin)
