# Generated by Django 3.1.2 on 2020-11-09 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20201109_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='poster',
            field=models.ForeignKey(db_column='user', default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.user'),
            preserve_default=False,
        ),
    ]
