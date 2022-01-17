# Generated by Django 4.0.1 on 2022-01-14 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('transaction_status', models.CharField(choices=[('C', 'closed'), ('R', 'reversed'), ('P', 'pending')], max_length=1)),
                ('approbal_status', models.BooleanField(default=False)),
                ('final_charge', models.BooleanField(default=False)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transactions.company', verbose_name='Company name')),
            ],
        ),
    ]
