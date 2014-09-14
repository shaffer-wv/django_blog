from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.dates import MonthArchiveView
from blogengine.models import Category, Post, Tag

# Create your views here.
# class PostListView(ListView):

# 	model = Post

# 	def get_context_data(self, **kwargs):
# 		context = super(PostListView, self).get_context_data(**kwargs)
# 		context['post_list'] = Post.objects.all()

# 		first_post = context['post_list'][0]
# 		post_info = first_post.pub_date.strftime("%m")
# 		print post_info

# 		month_archives = {}
# 		for post in context['post_list']:
# 			if post.pub_date.year not in month_archives:
# 				month_archives[post.pub_date.year] = [post.pub_date.strftime("%B")]
# 			else:
# 				if post.pub_date.strftime("%B") not in month_archives[post.pub_date.year]:
# 					month_archives[post.pub_date.year].append(post.pub_date.strftime("%B"))

		
# 		context['month_archives'] = month_archives
# 		return context

class CategoryListView(ListView):
	def get_queryset(self):
		slug = self.kwargs['slug']
		try:
			category = Category.objects.get(slug=slug)
			return Post.objects.filter(category=category)
		except Category.DoesNotExist:
			return Post.objects.none()

class TagListView(ListView):
	def get_queryset(self):
		slug = self.kwargs['slug']
		try:
			tag = Tag.objects.get(slug=slug)
			return tag.post_set.all()
		except Tag.DoesNotExist:
			return Post.objects.none()

class PostMonthArchiveView(MonthArchiveView):
	queryset = Post.objects.all()
	date_field = 'pub_date'
	make_object_list = True