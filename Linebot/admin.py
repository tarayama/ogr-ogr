from django.contrib import admin
from Linebot.models import LineAccount

# Register your models here.

class LineAccountAdmin(admin.ModelAdmin):
    pass

admin.site.register(LineAccount, LineAccountAdmin)
