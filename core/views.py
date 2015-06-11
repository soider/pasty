# -*- coding: utf-8 -*-
import core.tasks

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from core.models import Pasty
from core.models import Source


def home(request):
    """Index"""
    return render(request, 'core/index.html')


def one(request):
    """Returns one pastry, used from javascript for page updates"""
    p = Pasty.rnd()
    if p:
        context = {'text': p.text, 'source': p.source, 'title': p.source_title()}
        return render(request, 'core/pasty.html', context)
    else:
        return HttpResponse(u'<div class="box pasty">Нету пирожков :-(</div>')


@login_required
def sources(request):
    """Sources list"""
    sources = Source.objects.all()
    context = {'sources': sources }
    return render(request, 'core/sources.html', context)


@login_required
def sync(request):
    """Start synchronization process"""
    sources_id = request.POST.getlist('source')
    if sources_id:
        for src_id in sources_id:
            core.tasks.SyncTask().delay(src_id)
    messages.info(request, u"Синхронизация запущена!")
    return HttpResponseRedirect(reverse('sources'))


def add(request):
    """Creates unpublished pastry"""
    if request.method == 'POST':
        pasty_body = request.POST['pasty_body']
        Pasty(text=pasty_body).save()
        messages.info(request, u"Ваш пирожок будет отправлен на модерацию")
        return HttpResponseRedirect(reverse('add'))
    else:
        return render(request, 'core/add.html')


