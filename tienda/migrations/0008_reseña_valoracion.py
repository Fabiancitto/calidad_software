# Generated by Django 5.1.2 on 2024-10-26 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0007_reseña'),
    ]

    operations = [
        migrations.AddField(
            model_name='reseña',
            name='valoracion',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
            preserve_default=False,
        ),
    ]
