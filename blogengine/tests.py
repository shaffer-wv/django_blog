from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from blogengine.models import Post, Category, Tag
import markdown2 as markdown

class PostTest(TestCase):
	def test_create_tag(self):
		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)
		only_tag = all_tags[0]
		self.assertEquals(only_tag, tag)

		self.assertEquals(only_tag.name, 'python')
		self.assertEquals(only_tag.description, 'The Python programming language')

	def test_create_category(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)
		only_category = all_categories[0]
		self.assertEquals(only_category, category)

		self.assertEquals(only_category.name, 'python')
		self.assertEquals(only_category.description, 'The Python programming language')


	def test_create_post(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()

		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.category = category

		post.save()

		# Add tags
		post.tags.add(tag)
		post.save()

		# Retrieve new post
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Check attributes
		self.assertEquals(only_post.title, 'My first post')
		self.assertEquals(only_post.text, 'This is my first blog post')
		self.assertEquals(only_post.slug, 'my-first-post')
		self.assertEquals(only_post.site.name, 'example.com')
		self.assertEquals(only_post.site.domain, 'example.com')
		self.assertEquals(only_post.pub_date.day, post.pub_date.day)
		self.assertEquals(only_post.pub_date.month, post.pub_date.month)
		self.assertEquals(only_post.pub_date.year, post.pub_date.year)
		self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
		self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
		self.assertEquals(only_post.pub_date.second, post.pub_date.second)
		self.assertEquals(only_post.category.name, 'python')
		self.assertEquals(only_post.category.description, 'The Python programming language')

		# Check tags
		post_tags = only_post.tags.all()
		self.assertEquals(len(post_tags), 1)
		only_post_tag = post_tags[0]
		self.assertEquals(only_post_tag, tag)
		self.assertEquals(only_post_tag.name, 'python')
		self.assertEquals(only_post_tag.description, 'The Python programming language')

class BaseAcceptanceTest(LiveServerTestCase):
	def setUp(self):
		self.client = Client()


class AdminTest(BaseAcceptanceTest):
	fixtures = ['users.json']

	def test_login(self):
		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)
		self.assertTrue('Log in' in response.content)

		self.client.login(username='bobsmith', password="password")

		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)
		self.assertTrue('Log out' in response.content)

	def test_logout(self):
		self.client.login(username='bobsmith', password="password")

		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)
		self.assertTrue('Log out' in response.content)

		self.client.logout()

		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)
		self.assertTrue('Log in' in response.content)

	def test_create_post(self):
		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		self.client.login(username='bobsmith', password="password")

		response = self.client.get('/admin/blogengine/post/add/')
		self.assertEquals(response.status_code, 200)

		# Create new post
		response = self.client.post('/admin/blogengine/post/add/', {
			'title': 'My first post',
			'text': 'This is my first post',
			'pub_date_0': '2013-12-28',
			'pub_date_1': '22:00:04',
			'slug': 'my-first-post',
			'site': '1',
			'category': '1',
			'tags': '1',
			},
			follow=True
			)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('added successfully' in response.content)

		# Check new post in database
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

	def test_edit_post(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.save()
		post.tags.add(tag)
		post.save()

		self.client.login(username='bobsmith', password="password")

		# Edit post
		response = self.client.post('/admin/blogengine/post/1/', {
			'title': 'My second post',
			'text': 'This is my second blog post',
			'pub_date_0': '2013-12-28',
			'pub_date_1': '22:00:04',
			'slug': 'my-second-post',
			'site': '1',
			'category': '1',
			'tags': '1',
			},
			follow=True
			)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('changed successfully' in response.content)

		# Check post amended
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post.title, 'My second post')
		self.assertEquals(only_post.text, 'This is my second blog post')

	def test_delete_post(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.category = category
		post.save()
		post.tags.add(tag)
		post.save()

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

		self.client.login(username='bobsmith', password="password")

		# Delete the post
		response = self.client.post('/admin/blogengine/post/1/delete/', {
			'post': 'yes'
			}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('deleted successfully' in response.content)

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 0)

	def test_create_category(self):
		self.client.login(username='bobsmith', password="password")

		response = self.client.get('/admin/blogengine/category/add/')
		self.assertEquals(response.status_code, 200)

		# Create new category
		response = self.client.post('/admin/blogengine/category/add/', {
			'name': 'python',
			'description': 'The Python programming language',
			},
			follow=True
			)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('added successfully' in response.content)

		# Check new post in database
		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)

	def test_edit_category(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		self.client.login(username='bobsmith', password="password")

		# Edit category
		response = self.client.post('/admin/blogengine/category/1/', {
			'name': 'java',
			'description': 'The Java programming language',
			},
			follow=True
			)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('changed successfully' in response.content)

		# Check category amended
		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)
		only_category = all_categories[0]
		self.assertEquals(only_category.name, 'java')
		self.assertEquals(only_category.description, 'The Java programming language')

	def test_delete_category(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		self.client.login(username='bobsmith', password="password")

		response = self.client.post('/admin/blogengine/category/1/delete/', {
			'post': 'yes'
			}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('deleted successfully' in response.content)

		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 0)

	def test_create_tag(self):
		self.client.login(username='bobsmith', password="password")

		response = self.client.get('/admin/blogengine/tag/add/')
		self.assertEquals(response.status_code, 200)

		response = self.client.post('/admin/blogengine/tag/add/', {
			'name': 'python',
			'description': 'The Python programming language'
			}, follow=True)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('added successfully' in response.content)

		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)

	def test_edit_tag(self):
		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		self.client.login(username='bobsmith', password="password")

		response = self.client.post('/admin/blogengine/tag/1/', {
			'name': 'java',
			'description': 'The Java programming language'
			}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('changed successfully' in response.content)

		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)
		only_tag = all_tags[0]
		self.assertEquals(only_tag.name, 'java')
		self.assertEquals(only_tag.description, 'The Java programming language')

	def test_delete_tag(self):
		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		self.client.login(username='bobsmith', password="password")

		response = self.client.post('/admin/blogengine/tag/1/')
		self.assertEquals(response.status_code, 200)

		response = self.client.post('/admin/blogengine/tag/1/delete/', {
			'post': 'yes'
			}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('deleted successfully' in response.content)

		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 0)


class PostViewTest(BaseAcceptanceTest):
	def test_index_view(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'java'
		tag.description = 'The Java programming language'
		tag.save()

		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.category = category
		post.save()
		post.tags.add(tag)
		post.save()

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)

		self.assertTrue(post.title in response.content)
		self.assertTrue(markdown.markdown(post.text) in response.content)
		self.assertTrue(post.category.name in response.content)

		post_tag = all_posts[0].tags.all()[0]
		self.assertTrue(post_tag.name in response.content)

		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

	def test_individual_post(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'java'
		tag.description = 'The Java programming language'
		tag.save()

		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.category = category
		post.save()
		post.tags.add(tag)
		post.save()

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		post_url = only_post.get_absolute_url()

		response = self.client.get(post_url)
		self.assertEquals(response.status_code, 200)

		self.assertTrue(post.title in response.content)
		self.assertTrue(markdown.markdown(post.text) in response.content)
		self.assertTrue(post.category.name in response.content)

		post_tag = all_posts[0].tags.all()[0]
		self.assertTrue(post_tag.name in response.content)

		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

	def test_category_page(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.category = category
		post.save()

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		category_url = post.category.get_absolute_url()

		# Fetch the category
		response = self.client.get(category_url)
		self.assertEquals(response.status_code, 200)

		self.assertTrue(post.category.name in response.content)
		self.assertTrue(post.title in response.content)

	def test_tag_page(self):
		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.save()
		post.tags.add(tag)
		post.save()

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		tag_url = post.tags.all()[0].get_absolute_url()

		response = self.client.get(tag_url)
		self.assertEquals(response.status_code, 200)

		self.assertTrue(post.tags.all()[0].name in response.content)

		self.assertTrue(post.text in response.content)

		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

	def test_nonexistent_category_page(self):
		category_url = '/category/blah/'
		response = self.client.get(category_url)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('No posts to show' in response.content)

	def test_nonexistent_tag_page(self):
		tag_url = '/tag/blah/'
		response = self.client.get(tag_url)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('No posts to show' in response.content)

class FlatPageViewTest(BaseAcceptanceTest):
	def test_create_flat_page(self):
		page = FlatPage()
		page.url = '/about/'
		page.title = 'About me'
		page.content = 'All about me'
		page.save()

		page.sites.add(Site.objects.all()[0])
		page.save()

		all_pages = FlatPage.objects.all()
		self.assertEquals(len(all_pages), 1)
		only_page = all_pages[0]
		self.assertEquals(only_page, page)

		self.assertEquals(only_page.url, '/about/')
		self.assertEquals(only_page.title, 'About me')
		self.assertEquals(only_page.content, 'All about me')

		page_url = only_page.get_absolute_url()

		response = self.client.get(page_url)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('About me' in response.content)
		self.assertTrue('All about me' in response.content)
