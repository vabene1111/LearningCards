# Generated by Django 3.0.2 on 2020-01-29 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Cards', '0005_questioncache'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TestQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('SUCCESS', 'Success'), ('FAIL', 'Fail')], max_length=128, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cards.Question')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cards.Test')),
            ],
        ),
    ]
