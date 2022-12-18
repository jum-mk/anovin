from django.contrib.sitemaps import Sitemap
from .models import Tutorial


class TutorialSitemap(Sitemap):
    def items(self):
        return Tutorial.objects.all()

    def location(self, obj):
        return '/tutorials/' + str(obj.slug)
