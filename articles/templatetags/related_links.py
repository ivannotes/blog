from django import template
from django.core.cache import cache
from articles.models import RelatedLink

register = template.Library()

def related_links():

    cache_key = 'related_links'
    links = cache.get(cache_key)
    if links is None:
	links = RelatedLink.objects.all();
	if len(links) == 0:
	    return {}
	cache.set(cache_key, links, 3600)

    return {'links': links}

register.inclusion_tag('articles/_related_links.html')(related_links)
