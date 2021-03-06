# Generated by Django 2.2.4 on 2019-09-16 12:59

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hadith',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, verbose_name='نام شخصیت ')),
                ('content', models.TextField(verbose_name='متن حدیث ')),
                ('picture', models.ImageField(upload_to='Hadith-pic/', verbose_name='تصویر ')),
            ],
            options={
                'verbose_name': 'احادیث',
                'verbose_name_plural': 'احادیث',
            },
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=128, verbose_name='موضوع ')),
                ('content', models.TextField(verbose_name='محتوا ')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='news-pic/', verbose_name='تصویر ')),
            ],
            options={
                'verbose_name': 'اخبار',
                'verbose_name_plural': 'اخبار',
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('small_text', models.TextField(verbose_name='متن کوچکتر ')),
                ('bold_text', models.TextField(verbose_name='متن بولد ')),
                ('picture', models.ImageField(upload_to='slider-pic/', verbose_name='تصویر ')),
                ('status', models.CharField(choices=[('Inactive', 'غیر فعال'), ('Active', 'فعال')], default='Inactive', max_length=32, verbose_name='وضعیت ')),
            ],
            options={
                'verbose_name': 'اسلایدر',
                'verbose_name_plural': 'اسلایدر',
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('deceased_id', models.CharField(blank=True, editable=False, max_length=6, null=True)),
                ('buyer_id', models.CharField(blank=True, editable=False, max_length=6, null=True)),
                ('presenter_id', models.CharField(blank=True, editable=False, max_length=6, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
