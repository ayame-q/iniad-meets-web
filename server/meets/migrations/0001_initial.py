# Generated by Django 3.0.5 on 2020-04-24 00:12

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
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
                ('student_id', models.CharField(default='', max_length=10, verbose_name='学籍番号')),
                ('name', models.CharField(default='', max_length=40, verbose_name='本名')),
                ('display_name', models.CharField(default='No name', max_length=20, verbose_name='公開名')),
                ('is_display_name_initialized', models.BooleanField(default=False, verbose_name='公開名初期化済み')),
                ('entry_year', models.IntegerField(blank=True, null=True, verbose_name='入学年度')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime, verbose_name='作成日')),
                ('is_student', models.BooleanField(default=True, verbose_name='学生か')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
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
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='サークル名')),
                ('leader_name', models.CharField(default='', max_length=50, verbose_name='代表者名')),
                ('is_using_entry_form', models.BooleanField(default=True, verbose_name='内部エントリーフォームを利用する')),
                ('entry_form_url', models.URLField(blank=True, null=True, verbose_name='エントリーフォームURL')),
                ('panflet_url', models.URLField(blank=True, null=True, verbose_name='サークル資料URL')),
                ('website_url', models.URLField(blank=True, null=True, verbose_name='WebサイトURL')),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='メールアドレス')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime, verbose_name='登録日')),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='meets.Circle', verbose_name='サークル')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
        migrations.AddField(
            model_name='circle',
            name='admin_users',
            field=models.ManyToManyField(blank=True, related_name='admin_circles', to='meets.UserRole'),
        ),
        migrations.AddField(
            model_name='circle',
            name='staff_users',
            field=models.ManyToManyField(blank=True, related_name='staff_circles', to='meets.UserRole'),
        ),
        migrations.CreateModel(
            name='ChatLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='コメント')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime, verbose_name='作成日')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='meets.ChatLog', verbose_name='返信先')),
                ('receiver_circle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='meets.Circle', verbose_name='宛先サークル')),
                ('send_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_logs', to=settings.AUTH_USER_MODEL, verbose_name='送信者')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userinfo', to='meets.UserRole', verbose_name='権限'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]