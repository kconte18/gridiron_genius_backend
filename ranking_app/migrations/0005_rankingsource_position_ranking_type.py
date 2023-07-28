# Generated by Django 3.2.5 on 2023-07-27 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking_app', '0004_alter_player_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='rankingsource',
            name='position_ranking_type',
            field=models.CharField(choices=[('QB', 'QuarterBack'), ('RB', 'RunningBack'), ('WR', 'WideReceiver'), ('TE', 'TightEnd'), ('DEF', 'Defense'), ('K', 'Kicker'), ('OVERALL', 'Overall')], default='K', max_length=7),
            preserve_default=False,
        ),
    ]