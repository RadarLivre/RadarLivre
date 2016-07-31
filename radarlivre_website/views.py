import time
from django.shortcuts import render, get_object_or_404
from radarlivre_api.models import About, Software, Contrib


def index(request):
    return render(request, 'website/rl_index.html', {'page_index': True})


def downloads_index(request):
    softwares = Software.objects.order_by('downloads')
    return render(
        request,
        'website/rl_about_index.html',
        {'page_softwares': True, 'has_footer': True, 'softwares': softwares}
    )


def contrib(request):
    now = (time.time()) * 1000
    contribs = Contrib.objects.all().filter(
        timestamp__gte=now - 60 * 60 * 1000
    )
    return render(
        request,
        'website/rl_contrib.html',
        {'page_contrib': True, 'has_footer': True, 'contribs': contribs}
    )


def about_index(request):
    abouts = About.objects.order_by('index')
    return render(
        request,
        'website/rl_about_index.html',
        {'page_about': True, 'has_footer': True, 'abouts': abouts}
    )


def about(request, pk):
    about = get_object_or_404(About, pk=pk)
    abouts = About.objects.exclude(pk=pk).order_by('index')
    return render(
        request,
        'website/rl_about.html',
        {
            'page_about': True,
            'has_footer': True,
            'about': about,
            'abouts': abouts
        }
    )
