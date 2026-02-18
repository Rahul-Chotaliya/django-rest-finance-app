from django.db import migrations
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from decimal import Decimal
import datetime


def seed_data(apps, schema_editor):
    """
    Seeds production data into the database.
    Creates categories, demo user, and realistic asset data.
    """
    Category = apps.get_model('tradehub', 'Category')
    Asset = apps.get_model('tradehub', 'Asset')
    User = apps.get_model('auth', 'User')

    # Create categories if they don't exist
    categories = {
        'crypto': Category.objects.get_or_create(
            slug='crypto',
            defaults={'name': 'Cryptocurrency'}
        )[0],
        'stocks': Category.objects.get_or_create(
            slug='stocks',
            defaults={'name': 'Stocks'}
        )[0],
        'bonds': Category.objects.get_or_create(
            slug='bonds',
            defaults={'name': 'Bonds'}
        )[0],
        'real-estate': Category.objects.get_or_create(
            slug='real-estate',
            defaults={'name': 'Real Estate'}
        )[0],
    }

    # Create demo user if doesn't exist
    demo_user, created = User.objects.get_or_create(
        username='demo',
        defaults={
            'email': 'demo@example.com',
            'first_name': 'Demo',
            'last_name': 'User',
            'password': make_password('demo123456'),  # Hash password here
        }
    )

    # Seed assets only if none exist
    if Asset.objects.filter(user=demo_user).exists():
        return  # Don't duplicate data

    # Cryptocurrency assets
    assets_data = [
        {
            'name': 'Bitcoin',
            'category_slug': 'crypto',
            'amount': '0.40',
            'cost': '15000.00',
            'ort_usd': '37500.00',
            'logs': [
                {'type': 'buy', 'quantity': '0.40', 'price': '37500.00', 'date': '2025-06-15'},
            ]
        },
        {
            'name': 'Ethereum',
            'category_slug': 'crypto',
            'amount': '5.00',
            'cost': '11250.00',
            'ort_usd': '17250.00',
            'logs': [
                {'type': 'buy', 'quantity': '5.00', 'price': '2250.00', 'date': '2025-07-10'},
            ]
        },
        {
            'name': 'Cardano',
            'category_slug': 'crypto',
            'amount': '1500.00',
            'cost': '750.00',
            'ort_usd': '1425.00',
            'logs': [
                {'type': 'buy', 'quantity': '1500.00', 'price': '0.50', 'date': '2025-08-20'},
            ]
        },
        # Stock assets
        {
            'name': 'Apple Inc.',
            'category_slug': 'stocks',
            'amount': '50.00',
            'cost': '7500.00',
            'ort_usd': '9787.50',
            'logs': [
                {'type': 'buy', 'quantity': '50.00', 'price': '150.00', 'date': '2024-03-01'},
            ]
        },
        {
            'name': 'Microsoft Corporation',
            'category_slug': 'stocks',
            'amount': '30.00',
            'cost': '9300.00',
            'ort_usd': '13065.00',
            'logs': [
                {'type': 'buy', 'quantity': '30.00', 'price': '310.00', 'date': '2024-05-10'},
            ]
        },
        {
            'name': 'Tesla Inc.',
            'category_slug': 'stocks',
            'amount': '20.00',
            'cost': '4900.00',
            'ort_usd': '5706.00',
            'logs': [
                {'type': 'buy', 'quantity': '20.00', 'price': '245.00', 'date': '2024-07-15'},
            ]
        },
        {
            'name': 'Alphabet Inc.',
            'category_slug': 'stocks',
            'amount': '15.00',
            'cost': '2100.00',
            'ort_usd': '2736.00',
            'logs': [
                {'type': 'buy', 'quantity': '15.00', 'price': '140.00', 'date': '2024-09-22'},
            ]
        },
        # Bond assets
        {
            'name': 'US Treasury Bond 10Y',
            'category_slug': 'bonds',
            'amount': '10000.00',
            'cost': '10000.00',
            'ort_usd': '10200.00',
            'logs': [
                {'type': 'buy', 'quantity': '10000.00', 'price': '1.00', 'date': '2024-01-15'},
            ]
        },
        {
            'name': 'IBM Corporate Bond',
            'category_slug': 'bonds',
            'amount': '5000.00',
            'cost': '5000.00',
            'ort_usd': '4900.00',
            'logs': [
                {'type': 'buy', 'quantity': '5000.00', 'price': '1.00', 'date': '2024-02-28'},
            ]
        },
        # Real Estate asset
        {
            'name': 'Realty Income Corp REITs',
            'category_slug': 'real-estate',
            'amount': '200.00',
            'cost': '13100.00',
            'ort_usd': '15840.00',
            'logs': [
                {'type': 'buy', 'quantity': '200.00', 'price': '65.50', 'date': '2024-04-10'},
            ]
        },
    ]

    # Create assets
    for asset_data in assets_data:
        category = categories[asset_data['category_slug']]
        logs = asset_data.pop('logs', [])
        category_slug = asset_data.pop('category_slug')
        
        # Skip if asset already exists for this user
        if Asset.objects.filter(
            user=demo_user,
            name=asset_data['name'],
            category=category
        ).exists():
            continue
        
        # Create a simple slug from name (autoslug will regenerate on save in real usage)
        simple_slug = asset_data['name'].lower().replace(' ', '-')[:30]
        
        # Create asset (convert string amounts to Decimal)
        Asset.objects.create(
            user=demo_user,
            category=category,
            name=asset_data['name'],
            amount=Decimal(asset_data['amount']),
            cost=Decimal(asset_data['cost']),
            ort_usd=Decimal(asset_data['ort_usd']),
            logs=logs,  # logs is JSON-safe with string values
            slug=simple_slug,
        )


def reverse_seed(apps, schema_editor):
    """
    Removes seeded data on reverse migration.
    """
    User = apps.get_model('auth', 'User')
    Asset = apps.get_model('tradehub', 'Asset')
    Category = apps.get_model('tradehub', 'Category')
    
    # Remove demo user and associated assets
    try:
        demo_user = User.objects.get(username='demo')
        Asset.objects.filter(user=demo_user).delete()
        demo_user.delete()
    except User.DoesNotExist:
        pass
    
    # Remove categories (optional—comment out to keep categories)
    # Category.objects.filter(slug__in=['crypto', 'stocks', 'bonds', 'real-estate']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tradehub', '0003_alter_asset_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_seed),
    ]
