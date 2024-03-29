# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-10-09 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('published_date', models.DateField(blank=True, null=True)),
                ('page_count', models.IntegerField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=10, null=True)),
                ('authors', models.ManyToManyField(blank=True, to='book.Author')),
            ],
        ),
        migrations.CreateModel(
            name='ImageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_thumbnail', models.URLField()),
                ('thumbnail', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='IndustryIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier_type', models.CharField(max_length=10)),
                ('identifier', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='image_links',
            field=models.ManyToManyField(blank=True, to='book.ImageLink'),
        ),
        migrations.AddField(
            model_name='book',
            name='industry_identifiers',
            field=models.ManyToManyField(blank=True, to='book.IndustryIdentifier'),
        ),
    ]
