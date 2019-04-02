# Generated by Django 2.0.3 on 2019-04-02 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wellth_water', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wellth_water.Users')),
            ],
        ),
    ]
