
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_remove_candidateprofile_aadhar_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidateprofile',
            name='secondary_qualification',
        ),
        migrations.RemoveField(
            model_name='candidateprofile',
            name='secondary_duration',
        ),
        migrations.RemoveField(
            model_name='candidateprofile',
            name='secondary_credits',
        ),
        migrations.RemoveField(
            model_name='candidateprofile',
            name='secondary_viva_marks',
        ),
        migrations.RemoveField(
            model_name='candidateprofile',
            name='secondary_practical_marks',
        ),
    ]
