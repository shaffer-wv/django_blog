from django.contrib import admin
import models

class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}

admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Post, PostAdmin)

# Register your models here.
