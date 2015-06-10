# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from core.models import Pasty
from core.models import Source
from core.sync import sync_rss_source


def home(request):
    return render(request, 'core/index.html')


def one(request):
    p = Pasty.rnd()
    if p:
        context = {'text': p.text, 'source': p.source, 'title': p.source_title()}
        return render(request, 'core/pasty.html', context)
    else:
        return HttpResponse(u'<div class="box pasty">Нету пирожков :-(</div>')


@login_required
def sources(request):
    sources = Source.objects.all()
    context = {'sources': sources }
    return render(request, 'core/sync.html', context)


@login_required
def sync(request):
    sources_id = request.POST.getlist('source')
    if sources_id:
        for src_id in sources_id:
            source = Source.objects.get(pk=src_id)
            sync_rss_source(source)
    return HttpResponseRedirect(reverse('sources'))


def add(request):
    if request.method == 'POST':
        pasty_body = request.POST['pasty_body']
        Pasty(text=pasty_body).save()
        messages.info(request, u"Ваш пирожок будет отправлен на модерацию")
        return HttpResponseRedirect(reverse('add'))
    else:
        return render(request, 'core/add.html')


