import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect, Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from articles.models import Article, Tag
from datetime import datetime

ARTICLE_PAGINATION = getattr(settings, 'ARTICLE_PAGINATION', 20)
ARTICLE_INDEX_PAGINATION = getattr(settings, 'ARTICLE_INDEX_PAGINATION', 2)

log = logging.getLogger('articles.views')


def display_index(request):
    """
	Display index pages
	"""
    context = {'request': request}
    articles = Article.objects.live(user=request.user)
    template = 'articles/article_list_with_detail.html'
    paginator = Paginator(articles, ARTICLE_INDEX_PAGINATION)

    try:
        page = paginator.page(1)
    except EmptyPage:
        raise Http404

    context.update({'page_obj': page})
    log.debug('get there %s' % paginator)
    response = render(request, template, context)
    return response


def display_about_me(request):
    """
	Display about me
	"""
    context = {
        'request': request,
        'disqus_forum': getattr(settings, 'DISQUS_FORUM_SHORTNAME', None)
    }
    template = 'articles/about_me.html'
    response = render(request, template, context)
    return response


def display_blog_page(request,
                      tag=None,
                      username=None,
                      year=None,
                      month=None,
                      page=1):
    """
    Handles all of the magic behind the pages that list articles in any way.
    Yes, it's dirty to have so many URLs go to one view, but I'd rather do that
    than duplicate a bunch of code.  I'll probably revisit this in the future.
    """

    context = {
        'request': request,
        'disqus_forum': getattr(settings, 'DISQUS_FORUM_SHORTNAME', None)
    }

    if tag:
        try:
            tag = get_object_or_404(Tag, slug__iexact=tag)
        except Http404:
            # for backwards-compatibility
            tag = get_object_or_404(Tag, name__iexact=tag)

        articles = tag.article_set.live(user=request.user).select_related()
        template = 'articles/display_tag.html'
        context['tag'] = tag

    elif username:
        # listing articles by a particular author
        user = get_object_or_404(User, username=username)
        articles = user.article_set.live(user=request.user)
        template = 'articles/by_author.html'
        context['author'] = user

    elif year and month:
        # listing articles in a given month and year
        year = int(year)
        month = int(month)
        articles = Article.objects.live(
            user=request.user).select_related().filter(
                publish_date__year=year, publish_date__month=month)
        template = 'articles/in_month.html'
        context['month'] = datetime(year, month, 1)

    else:
        # listing articles with no particular filtering
        articles = Article.objects.live(user=request.user)
        template = 'articles/article_list.html'

    # paginate the articles
    paginator = Paginator(
        articles, ARTICLE_PAGINATION, orphans=int(ARTICLE_PAGINATION / 4))
    try:
        page = paginator.page(page)
    except EmptyPage:
        raise Http404

    context.update({'paginator': paginator, 'page_obj': page})
    response = render(request, template, context)

    return response


def display_article(request,
                    year,
                    slug,
                    template='articles/article_detail.html'):
    """Displays a single article."""

    try:
        article = Article.objects.live(user=request.user).get(
            publish_date__year=year, slug=slug)
    except Article.DoesNotExist:
        raise Http404

    # make sure the user is logged in if the article requires it
    if article.login_required and not request.user.is_authenticated():
        return HttpResponseRedirect(
            reverse('auth_login') + '?next=' + request.path)

    context = {
        'article': article,
        'disqus_forum': getattr(settings, 'DISQUS_FORUM_SHORTNAME', None),
    }
    response = render(request, template, context)

    return response


def redirect_to_article(request, year, month, day, slug):
    # this is a little snippet to handle URLs that are formatted the old way.
    article = get_object_or_404(Article, publish_date__year=year, slug=slug)
    return HttpResponsePermanentRedirect(article.get_absolute_url())


def ajax_tag_autocomplete(request):
    """Offers a list of existing tags that match the specified query"""

    if 'q' in request.GET:
        q = request.GET['q']
        key = 'ajax_tag_auto_%s' % q
        response = cache.get(key)

        if response is not None:
            return response

        tags = list(Tag.objects.filter(name__istartswith=q)[:10])
        response = HttpResponse(u'\n'.join(tag.name for tag in tags))
        cache.set(key, response, 300)

        return response

    return HttpResponse()
