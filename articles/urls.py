from django.urls import re_path, path
from django.contrib.sitemaps.views import sitemap

from articles import views
from articles.feeds import TagFeed, LatestEntries, TagFeedAtom, LatestEntriesAtom
from articles.models import Article
from django.contrib.sitemaps import GenericSitemap

tag_rss = TagFeed()
latest_rss = LatestEntries()
tag_atom = TagFeedAtom()
latest_atom = LatestEntriesAtom()

urlpatterns = [
    re_path(
        r'^(?P<year>\d{4})/(?P<month>.{3})/(?P<day>\d{1,2})/(?P<slug>.*)/$',
        views.redirect_to_article),
    re_path(
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page>\d+)/$',
        views.display_blog_page,
        name='articles_in_month_page'),
    re_path(
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.display_blog_page,
        name='articles_in_month'),
]

info_dict = {'queryset': Article.objects.all(), 'date_field': 'publish_date'}
sitemaps = {'blog': GenericSitemap(info_dict, priority=0.6)}
urlpatterns += [
    re_path(r'^$', views.display_index, name='articles_index'),
    path(
        'sitemap.xml',
        sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^blog/$', views.display_blog_page, name='articles_archive'),
    re_path(r'^about/$', views.display_about_me, name='articles_archive'),
    re_path(
        r'^page/(?P<page>\d+)/$',
        views.display_blog_page,
        name='articles_archive_page'),
    re_path(
        r'^tag/(?P<tag>.*)/page/(?P<page>\d+)/$',
        views.display_blog_page,
        name='articles_display_tag_page'),
    re_path(
        r'^tag/(?P<tag>.*)/$',
        views.display_blog_page,
        name='articles_display_tag'),
    re_path(
        r'^author/(?P<username>.*)/page/(?P<page>\d+)/$',
        views.display_blog_page,
        name='articles_by_author_page'),
    re_path(
        r'^author/(?P<username>.*)/$',
        views.display_blog_page,
        name='articles_by_author'),
    re_path(
        r'^(?P<year>\d{4})/(?P<slug>.*)/$',
        views.display_article,
        name='articles_display_article'),

    # AJAX
    re_path(
        r'^ajax/tag/autocomplete/$',
        views.ajax_tag_autocomplete,
        name='articles_tag_autocomplete'),

    # RSS
    re_path(
        r'^feeds/latest\.rss$', latest_rss, name='articles_rss_feed_latest'),
    re_path(r'^feeds/latest/$', latest_rss),
    re_path(
        r'^feeds/tag/(?P<slug>[\w_-]+)\.rss$',
        tag_rss,
        name='articles_rss_feed_tag'),
    re_path(r'^feeds/tag/(?P<slug>[\w_-]+)/$', tag_rss),

    # Atom
    re_path(
        r'^feeds/atom/latest\.xml$',
        latest_atom,
        name='articles_atom_feed_latest'),
    re_path(
        r'^feeds/atom/tag/(?P<slug>[\w_-]+)\.xml$',
        tag_atom,
        name='articles_atom_feed_tag'),
]
