from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_questionpaper_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionupload',
            name='category',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
