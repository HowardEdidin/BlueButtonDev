# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('appmgmt', '0008_auto_20151102_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='developers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
