# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Eleve',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_de_naissance', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MesActivite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_description_activite', models.CharField(max_length=200, verbose_name=b"Type D'activit\xc3\xa9")),
                ('full_description_activite', models.TextField(default=b'Description requise pour cette activit\xc3\xa9', verbose_name=b'Enonc\xc3\xa9 ')),
                ('docfile', models.FileField(upload_to=b'documents/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MesClasse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom_etablissement_text', models.CharField(max_length=200, verbose_name=b'mon \xc3\xa9tablissement')),
                ('annee_cours_dateint', models.IntegerField(default=2014, verbose_name=b'Ann\xc3\xa9e en cours')),
                ('niveau', models.IntegerField(verbose_name=b'Niveau')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MesSeance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_description_seance', models.CharField(max_length=200, verbose_name=b'Objet de la s\xc3\xa9ance')),
                ('full_description_seance', models.TextField(default=b'Description requise', verbose_name=b"Description d'une s\xc3\xa9ance ")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MesSequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_description_sequence', models.CharField(max_length=200, verbose_name=b'Nom de la s\xc3\xa9quence')),
                ('full_description_sequence', models.TextField(default=b'Description manquante', verbose_name=b"Description d'une s\xc3\xa9quence")),
                ('niveau_indicatif', models.IntegerField(null=True, verbose_name=b'Niveau', blank=True)),
                ('domaine', models.CharField(max_length=200, verbose_name=b'domaine/theme')),
                ('ma_classe', models.ForeignKey(blank=True, to='MonEtablissement.MesClasse', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='messeance',
            name='ma_sequence',
            field=models.ForeignKey(to='MonEtablissement.MesSequence'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mesactivite',
            name='ma_seance',
            field=models.ForeignKey(to='MonEtablissement.MesSeance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eleve',
            name='ma_classe',
            field=models.ForeignKey(to='MonEtablissement.MesClasse'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eleve',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
