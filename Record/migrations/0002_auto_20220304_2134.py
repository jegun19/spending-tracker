# Generated by Django 3.2.5 on 2022-03-04 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Record', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spendingtrs',
            name='category',
            field=models.CharField(choices=[('Food', 'FOOD'), ('Bills', 'BILLS'), ('Travel', 'TRAVEL'), ('Healthcare', 'HEALTHCARE'), ('Entertainment', 'ENTERTAINMENT'), ('Other', 'OTHER')], max_length=50, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='spendingtrs',
            name='currency',
            field=models.CharField(choices=[('NTD', 'NTD')], max_length=3, verbose_name='Currency'),
        ),
    ]
