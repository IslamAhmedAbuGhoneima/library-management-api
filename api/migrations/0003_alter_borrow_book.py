# Generated by Django 4.2.5 on 2023-09-27 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_book_borrowed_alter_borrow_book_alter_borrow_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.book'),
        ),
    ]
