from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_blog_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Blog URLs
    url(r'', include('blogengine.urls')),

    # Haystack / Search URLs
    url(r'^search/', include('haystack.urls')),

    # Flat pages
    url(r'', include('django.contrib.flatpages.urls')),
    
	
)
