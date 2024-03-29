# Generated by Django 4.2 on 2023-04-25 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('slug', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('cat_image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
    ]
