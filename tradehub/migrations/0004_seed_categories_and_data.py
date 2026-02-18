from django.db import migrations
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
        }
    )
    if created:
        demo_user.set_password('demo123456')
        demo_user.save()

    # Seed assets only if none exist
    if Asset.objects.filter(user=demo_user).exists():
        return  # Don't duplicate data

    # Cryptocurrency assets
    assets_data = [
        {
            'name': 'Bitcoin',
            'category_slug': 'crypto',
            'amount': Decimal('0.40'),
            'buy_price': Decimal('37500.00'),
            'current_price': Decimal('93750.00'),
            'logs': [
                {'type': 'buy', 'quantity': Decimal('0.40'), 'price': Decimal('37500.00'), 'date': '2025-06-15'},
            ]
        },
        {
            'name': 'Ethereum',
            'category_slug': 'crypto',
            'amount': Decimal('5.00'),
            'buy_price': Decimal('2250.00'),
            'current_price': Decimal('3450.00'),
            'logs': [
                {'type': 'buy', 'quantity': Decimal('5.00'), 'price': Decimal('2250.00'), 'date': '2025-07-10'},
            ]
        },
        {
            'name': 'Cardano',
            'category_slug': 'crypto',
            'amount': Decimal('1500.00'),
            'buy_price': Decimal('0.50'),
            'current_price': Decimal('0.95'),
            'logs': [
                {'type': 'buy', 'quantity': Decimal('1500.00'), 'price': Decimal('0.50'), 'date': '2025-08-20'},
            ]
        },
        # Stock assets
        {
            'name': 'Apple Inc.',
            'category_slug': 'stocks',
            'amount': Decimal('50.00'),
            'buy_price': Decimal('150.00'),
            'current_price': Decimal('195.75'),
            'logs': [
                {'type': 'buy', 'quantity': Decimal('50.00'), 'price': Decimal('150.00'), 'date': '2024-03-01'},
            ]
        },
        {
            'name': 'Microsoft Corporation',
            'category_slug': 'stocks',
            'amount': Decimal('30.00'),
            'buy_price': Decimal('310.00'),
            'current_price': Decimal('435.50'),
            'logs': [
                {'type': 'buy', 'quantity': Decimal('30.00'), 'price': Decimal('310.00'), 'date': '2024-05-10'},
            ]
        },
        {
            'name': 'Tesla Inc.',
            'category_slug': 'stocks',
            'amount': Decimal('20.00'),
            'buy_price': Decimal('245.00'),
            'current_price': Decimal('285.30'),
            'logs': [
                {'type': 'buy', 'quantity': Decimal('20.00'), 'price': Decimal('245.00'), 'date': '2024-07-15'},
            ]
        },
        {
            'name': 'Alphabet Inc.',
            'category_slug': 'stocks',
            'amount': Decimal('15.00'),
            'buy_price': Decimal('140.00'),
            'current_price': Decimal('182.40'),
            'logs': [
                {'type': 'buy', 'quantity': Decimal('15.00'), 'price': Decimal('140.00'), 'date': '2024-09-22'},
            ]
        },
        # Bond assets
        {
            'name': 'US Treasury Bond 10Y',
            'category_slug': 'bonds',
            'amount': Decimal('10000.00'),
            'buy_price': Decimal('1.00'),
            'current_price': Decimal('1.02'),
            'logs': [
                {'type': 'buy', 'quantity': Decimal('10000.00'), 'price': Decimal('1.00'), 'date': '2024-01-15'},
            ]
        },
        {
            'name': 'IBM Corporate Bond',
            'category_slug': 'bonds',
            'amount': Decimal('5000.00'),
            'buy_price': Decimal('1.00'),
            'current_price': Decimal('0.98'),
            'logs': [
                {'type': 'buy', 'quantity': Decimal('5000.00'), 'price': Decimal('1.00'), 'date': '2024-02-28'},
            ]
        },
        # Real Estate asset
        {
            'name': 'Realty Income Corp REITs',
            'category_slug': 'real-estate',
            'amount': Decimal('200.00'),
            'buy_price': Decimal('65.50'),
            'current_price': Decimal('79.20'),
            'logs': [
                {'type': 'buy', 'quantity': Decimal('200.00'), 'price': Decimal('65.50'), 'date': '2024-04-10'},
            ]
        },
    ]

    # Create assets
    for asset_data in assets_data:
        category = categories[asset_data['category_slug']]
        logs = asset_data.pop('logs', [])
        
        asset, created = Asset.objects.get_or_create(
            user=demo_user,
            name=asset_data['name'],
            category=category,
            defaults={
                'amount': asset_data['amount'],
                'buy_price': asset_data['buy_price'],
                'current_price': asset_data['current_price'],
                'transaction_logs': logs,
            }
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
