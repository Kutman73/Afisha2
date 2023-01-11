# Generated by Django 4.1.4 on 2022-12-21 08:10

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Режиссер',
                'verbose_name_plural': 'Режиссеры',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('duration', models.DurationField()),
                ('release_date', models.DateField()),
                ('creation_date', models.DateField(auto_now=True)),
                ('number', models.IntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movi', to='movie_app.director')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('stars', models.DecimalField(choices=[(Decimal('1.0'), '★☆☆☆☆ (1/5)'), (Decimal('2.0'), '★★☆☆☆ (2/5)'), (Decimal('3.0'), '★★★☆☆ (3/5)'), (Decimal('4.0'), '★★★★☆ (4/5)'), (Decimal('5.0'), '★★★★★ (5/5)')], decimal_places=1, default=3.0, max_digits=2)),
                ('creation_date', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='movie_app.movie')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
    ]
