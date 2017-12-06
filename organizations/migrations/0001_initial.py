# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 21:56
from __future__ import unicode_literals

import common.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', common.models.RequiredCharField(max_length=200, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex='^[^ ]+$')])),
                ('website', common.models.OptionalCharField(max_length=200, validators=[django.core.validators.URLValidator()])),
                ('email', common.models.OptionalCharField(max_length=200, validators=[django.core.validators.EmailValidator()])),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrganizationTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='organizations.Organization')),
            ],
            options={
                'verbose_name': 'organization Translation',
                'db_table': 'organizations_organization_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.AlterUniqueTogether(
            name='organizationtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]