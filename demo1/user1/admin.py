from django.contrib import admin

# Register your models here.
from .models import BookInfo,HeroInfo

class HeroInfoAdmin(admin.ModelAdmin):
    # 右侧过滤器栏
    list_display = ['id', 'btitle', 'bread', 'bcomment', 'bpub_date']


admin.site.register(BookInfo, HeroInfoAdmin)
admin.site.register(HeroInfo)