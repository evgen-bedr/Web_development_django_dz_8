# Generated by Django 5.0.6 on 2024-06-03 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='subtask',
            options={'ordering': ['-created_at'], 'verbose_name': 'SubTask'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-created_at'], 'verbose_name': 'Task'},
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='subtask',
            unique_together={('title',)},
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('title',)},
        ),
        migrations.AlterModelTable(
            name='category',
            table='task_manager_category',
        ),
        migrations.AlterModelTable(
            name='subtask',
            table='task_manager_subtask',
        ),
        migrations.AlterModelTable(
            name='task',
            table='task_manager_task',
        ),
    ]
