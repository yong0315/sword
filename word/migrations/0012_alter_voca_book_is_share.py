# Generated by Django 4.0.3 on 2023-11-20 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0011_word_voter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voca_book',
            name='is_share',
            field=models.BooleanField(default=True),
        ),
    ]
