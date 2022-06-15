# Generated by Django 4.0.3 on 2022-06-13 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import re_QA.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='file/document_list/document/', verbose_name='ファイル')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='file/photo_list/photo/', verbose_name='フォト')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='匿名', max_length=100, verbose_name='投稿者の名前')),
                ('comment', models.CharField(max_length=2000, verbose_name='コメント')),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('genre', models.CharField(max_length=20, verbose_name='質問のジャンル')),
                ('deadline', models.DateTimeField(default=re_QA.models.Topic.one_week, verbose_name='回答受付期限')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
        migrations.CreateModel(
            name='ValidationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, verbose_name='登録用コード')),
                ('purpose', models.CharField(max_length=30, verbose_name='使用目的')),
                ('source', models.CharField(max_length=30, verbose_name='紹介方法')),
            ],
        ),
        migrations.CreateModel(
            name='TopicReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='匿名', max_length=100, verbose_name='投稿者の名前')),
                ('comment', models.CharField(max_length=2000, verbose_name='コメント')),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='re_QA.topic', verbose_name='対象トピック')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resident_area', models.CharField(max_length=30, verbose_name='質問者の居住エリア')),
                ('resident_style', models.CharField(max_length=30, verbose_name='質問者の居住スタイル')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerUserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=30, verbose_name='ペンネーム')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=30, verbose_name='回答者の会社名')),
                ('approval', models.BooleanField(default=False, verbose_name='回答権利')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
    ]
