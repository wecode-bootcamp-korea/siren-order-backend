# Generated by Django 2.2.2 on 2019-07-18 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Drinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('english_name', models.CharField(max_length=50)),
                ('img_url', models.CharField(max_length=450)),
                ('only_ice', models.BooleanField(default=True)),
                ('oz_price', models.IntegerField(blank=True, default=0, null=True)),
                ('short_price', models.IntegerField(blank=True, default=0, null=True)),
                ('tall_price', models.IntegerField(blank=True, default=0, null=True)),
                ('grande_price', models.IntegerField(blank=True, default=0, null=True)),
                ('venti_price', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.CharField(max_length=400, null=True)),
                ('condition', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'drinks',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Categories')),
            ],
            options={
                'db_table': 'section',
            },
        ),
        migrations.CreateModel(
            name='Stuff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('english_name', models.CharField(max_length=50)),
                ('img_url', models.CharField(max_length=450)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('volume', models.CharField(max_length=4)),
                ('option', models.CharField(max_length=20, null=True)),
                ('description', models.CharField(max_length=400, null=True)),
                ('condition', models.CharField(max_length=200, null=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Section')),
            ],
            options={
                'db_table': 'stuff',
            },
        ),
        migrations.CreateModel(
            name='Hot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('english_name', models.CharField(max_length=50)),
                ('img_url', models.CharField(max_length=450)),
                ('description', models.CharField(max_length=400, null=True)),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Drinks')),
            ],
            options={
                'db_table': 'hot',
            },
        ),
        migrations.CreateModel(
            name='Foods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('english_name', models.CharField(max_length=50)),
                ('img_url', models.CharField(max_length=450)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.CharField(max_length=400, null=True)),
                ('condition', models.CharField(max_length=200, null=True)),
                ('option', models.BooleanField(default=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Section')),
            ],
            options={
                'db_table': 'foods',
            },
        ),
        migrations.AddField(
            model_name='drinks',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Section'),
        ),
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('english_name', models.CharField(max_length=50)),
                ('img_url', models.CharField(max_length=450)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('size', models.CharField(max_length=10)),
                ('weight', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=400, null=True)),
                ('condition', models.CharField(max_length=200, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Categories')),
            ],
            options={
                'db_table': 'cake',
            },
        ),
    ]
