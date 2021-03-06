# Generated by Django 4.0.1 on 2022-01-27 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_customuser_is_student_customuser_is_teacher_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_student',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_teacher',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='mailing_address',
        ),
        migrations.AddField(
            model_name='customuser',
            name='state',
            field=models.CharField(choices=[('Step 1', 'Step 1'), ('Step 2', 'Step 2'), ('Step 3', 'Step 3'), ('Completed', 'Completed')], default='Step 1', max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
