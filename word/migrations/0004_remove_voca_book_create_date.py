# Generated by Django 4.0.3 on 2023-11-08 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0003_rename_title_word_voca_book_remove_word_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voca_book',
            name='create_date',
        ),
    ]