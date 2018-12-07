# Generated by Django 2.1.3 on 2018-12-07 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20181207_1625'),
        ('main', '0003_kid_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredcourse',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.School'),
        ),
        migrations.AlterField(
            model_name='registeredcourse',
            name='tracker',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Tracker'),
        ),
    ]
