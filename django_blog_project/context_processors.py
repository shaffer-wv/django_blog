
from blogengine.models import Post

def month_archives(request):
	posts = Post.objects.all()
	month_archives = {}

	for post in posts:
		if post.pub_date.year not in month_archives:
				month_archives[post.pub_date.year] = [(post.pub_date.strftime("%B"), post.pub_date.month)]
		else:
			if (post.pub_date.strftime("%B"), post.pub_date.month) not in month_archives[post.pub_date.year]:
				month_archives[post.pub_date.year].append((post.pub_date.strftime("%B"), post.pub_date.month))

	print month_archives
	return {"month_archives": month_archives}

