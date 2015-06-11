# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_pasty_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pasty',
            options={'verbose_name': '\u041f\u0438\u0440\u043e\u0436\u043e\u043a', 'verbose_name_plural': '\u041f\u0438\u0440\u043e\u0436\u043a\u0438'},
        ),
        migrations.AlterModelOptions(
            name='source',
            options={'verbose_name': '\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a', 'verbose_name_plural': '\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438'},
        ),
    ]
