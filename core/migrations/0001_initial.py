from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('code', models.SlugField(max_length=32, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='InternalUserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('ms', 'MS User'), ('dev', 'Developer')], max_length=12)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.partner')),
            ],
            options={'ordering': ['sku'], 'unique_together': {('partner', 'sku')}},
        ),
        migrations.CreateModel(
            name='PartnerUserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.partner')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('location', models.CharField(max_length=200)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouses', to='core.partner')),
            ],
            options={'ordering': ['name'], 'unique_together': {('partner', 'name')}},
        ),
        migrations.CreateModel(
            name='StockTransferOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('done', 'Done')], default='pending', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('from_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_stos', to='core.warehouse')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.inventoryitem')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stos', to='core.partner')),
                ('to_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_stos', to='core.warehouse')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='WarehouseStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='core.inventoryitem')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='core.warehouse')),
            ],
            options={'unique_together': {('warehouse', 'item')}},
        ),
    ]
