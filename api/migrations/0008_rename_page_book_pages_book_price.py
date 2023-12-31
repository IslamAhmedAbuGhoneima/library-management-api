# Generated by Django 4.2.5 on 2023-10-07 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_book_page_alter_book_auther_alter_book_available'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='page',
            new_name='pages',
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
