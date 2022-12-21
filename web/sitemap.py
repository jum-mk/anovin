from django.contrib.sitemaps import Sitemap
from .models import Tutorial, Tag, Category


class TutorialSitemap(Sitemap):
    def items(self):
        return Tutorial.objects.all()

    def location(self, obj):
        return '/tutorial/' + str(obj.slug)


class TagSitemap(Sitemap):
    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return str(obj.get_absolute_url())


class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return str(obj.get_absolute_url())
