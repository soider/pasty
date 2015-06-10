# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pasty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442 \u043f\u0438\u0440\u043e\u0436\u043a\u0430')),
                ('date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438', blank=True)),
                ('source', models.URLField(verbose_name='\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a', blank=True)),
                ('votes', models.IntegerField(default=0, null=True, verbose_name='\u0413\u043e\u043b\u043e\u0441\u043e\u0432')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430')),
                ('url', models.URLField(verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('sync_url', models.URLField(verbose_name='URL \u0441\u0438\u043d\u0445\u0440\u043e\u043d\u0438\u0437\u0430\u0446\u0438\u0438', blank=True)),
                ('sync_date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u0441\u0438\u043d\u0445\u0440\u043e\u043d\u0438\u0437\u0430\u0446\u0438\u0438', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
