# Generated by Django 4.1.4 on 2023-03-24 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_service', '0013_alter_engfixer_input_sentence'),
    ]

    operations = [
        migrations.AddField(
            model_name='engfixer',
            name='fixed_result_JSON',
            field=models.JSONField(default=None),
            preserve_default=False,
        ),
    ]
