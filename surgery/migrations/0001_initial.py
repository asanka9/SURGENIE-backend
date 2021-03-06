# Generated by Django 4.0.1 on 2022-02-08 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurgeryResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.resource')),
                ('surgeon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.surgeon')),
            ],
        ),
        migrations.CreateModel(
            name='Surgery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_minute', models.IntegerField()),
                ('end_minute', models.IntegerField()),
                ('start_hour', models.IntegerField()),
                ('end_hour', models.IntegerField()),
                ('date', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('predicted_time', models.IntegerField()),
                ('estimated_time', models.IntegerField()),
                ('real_time', models.IntegerField(blank=True)),
                ('is_completed', models.BooleanField(blank=True, default=False)),
                ('surgeon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.surgeon')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=10)),
                ('notes', models.TextField(default='')),
                ('age', models.IntegerField()),
                ('gender', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('height', models.IntegerField()),
                ('cancer', models.IntegerField()),
                ('cvd', models.IntegerField()),
                ('dementia', models.IntegerField()),
                ('diabetes', models.IntegerField()),
                ('digestive', models.IntegerField()),
                ('osteoarthritis', models.IntegerField()),
                ('pylogical', models.IntegerField()),
                ('pulmonary', models.IntegerField()),
                ('surgery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surgery.surgery')),
            ],
        ),
    ]
