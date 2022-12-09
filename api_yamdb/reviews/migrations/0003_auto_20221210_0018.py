# Generated by Django 2.2.16 on 2022-12-09 21:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20221209_0046'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10, message='Оценка должна быть не больше 10'), django.core.validators.MinValueValidator(1, message='Оценка не должна быть менее 1')]),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_review'),
        ),
    ]
