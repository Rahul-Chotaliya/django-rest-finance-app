"""
Models for the TradeHub application.

This module defines the core data models for portfolio management:
- Category: Asset categories (Cryptocurrency, Stocks, Bonds, etc.)
- Asset: Individual assets owned by users with transaction logs
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import string
import random
from decimal import Decimal, ROUND_HALF_UP

from autoslug import AutoSlugField


class Category(models.Model):
    """
    Asset Category Model
    
    Represents different categories of investments that users can track.
    Examples: Cryptocurrency, Stocks, Bonds, Real Estate
    
    Attributes:
        name (str): Human-readable category name (e.g., "Cryptocurrency")
        slug (str): URL-friendly identifier (e.g., "crypto")
    """
    name = models.CharField(
        max_length=1000,
        help_text="Category name (e.g., Cryptocurrency, Stocks)"
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        help_text="URL-friendly identifier (auto-generated from name)"
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        """String representation of the category"""
        return self.name
    
    def get_absolute_url(self):
        """Get the URL for this category's asset listing page"""
        return reverse('tradehub:asset_category', kwargs={'asset_category_slug': self.slug})


class Asset(models.Model):
    """
    Asset Model - Represents individual investments owned by users
    
    Each asset belongs to a user and category. Tracks amount held, cost basis,
    current USD value, and maintains a JSON log of all buy/sell transactions.
    
    Attributes:
        user (ForeignKey): User who owns this asset
        slug (AutoSlugField): Unique identifier for the asset
        category (ForeignKey): Category this asset belongs to
        name (str): Asset name (e.g., "Bitcoin", "Apple Inc.")
        amount (Decimal): Current quantity held (after all transactions)
        cost (Decimal): Total cost basis in USD
        ort_usd (Decimal): Current market value in USD
        logs (JSONField): Transaction history [{'type': 'buy'|'sell', 'amount': X, ...}]
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who owns this asset"
    )
    slug = AutoSlugField(
        populate_from='generate_random_slug',
        unique=True,
        null=True,
        blank=True,
        help_text="Auto-generated unique identifier"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Asset category (Crypto, Stocks, etc.)"
    )
    name = models.CharField(
        max_length=100,
        help_text="Asset name (e.g., Bitcoin, Apple Inc., US Treasury Bonds)"
    )
    amount = models.DecimalField(
        max_digits=50,
        decimal_places=10,
        default=Decimal('0'),
        help_text="Current quantity held (e.g., 0.5 for Bitcoin)"
    )
    cost = models.DecimalField(
        max_digits=100,
        decimal_places=2,
        default=Decimal('0'),
        help_text="Total cost basis in USD"
    )
    ort_usd = models.DecimalField(
        max_digits=100,
        decimal_places=10,
        default=Decimal('0'),
        help_text="Current market value in USD (ORT = average price)"
    )
    logs = models.JSONField(
        null=True,
        blank=True,
        default=list,
        help_text="JSON array of transaction logs with buy/sell records"
    )

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
        ordering = ['-id']
        unique_together = ('user', 'name', 'category')

    def __str__(self):
        """String representation showing user and asset name"""
        return f"{self.user.username} - {self.name}"

    def save(self, *args, **kwargs):
        """
        Custom save method to handle data validation and normalization
        
        - Converts None values to Decimal('0')
        - Ensures amount and cost are never negative
        - Initializes logs if empty
        - Prevents invalid state combinations
        """
        # Handle None values by converting to Decimal('0')
        if self.amount is None:
            self.amount = Decimal('0')
        if self.cost is None:
            self.cost = Decimal('0')
        if self.ort_usd is None:
            self.ort_usd = Decimal('0')
            
        # Normalize negative or zero amounts
        if self.amount <= 0:
            self.amount = Decimal('0')
            self.ort_usd = Decimal('0')
            self.cost = Decimal('0')
        
        # Ensure cost is never negative
        elif self.cost < 0:
            self.cost = Decimal('0')

        # Initialize transaction counters if logs are empty
        if self.logs is None or len(self.logs) < 1:
            self.buy_count = 0
            self.sell_count = 0

        super(Asset, self).save(*args, **kwargs)

    def generate_random_slug(self):
        """
        Generate a random 15-character slug for unique asset identification
        
        Uses only lowercase letters for URL safety and consistency.
        This is used by AutoSlugField to generate unique identifiers.
        
        Returns:
            str: Random 15-character string of lowercase letters
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(15))

    def get_absolute_url(self):
        """Get the URL for this asset's detail/transaction log page"""
        return reverse('tradehub:asset_logs', kwargs={'asset_slug': self.slug})

    @property
    def total_invested(self):
        """Calculate total amount invested in this asset"""
        return self.cost

    @property
    def current_value(self):
        """Get current market value in USD"""
        return self.ort_usd

    @property
    def gain_loss(self):
        """Calculate gain/loss in USD (current value - cost basis)"""
        return self.current_value - self.total_invested

    @property
    def gain_loss_percentage(self):
        """Calculate gain/loss as percentage"""
        if self.total_invested == 0:
            return Decimal('0')
        return (self.gain_loss / self.total_invested * 100)


    def get_absolute_url(self):
        return reverse('tradehub:asset_logs', kwargs={'asset_slug': self.slug})



    # COİN JSON -> {'İşlem: (buy or sell)','COİN Adeti:', 'TOTAL PARA:', 'KUR:', 'USD KARŞILIĞI:'}
    # HİSSE JSON -> {'İşlem: (buy or sell)','LOT Adeti:', 'TOTAL PARA:', 'KUR':,  'USD KARŞILIĞI:'}