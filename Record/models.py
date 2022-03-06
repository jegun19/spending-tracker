from django.db import models


# Create your models here.
class SpendingTrs(models.Model):
    currency_choices = (
        ('NTD', 'NTD'),
    )

    category_choices = (
        ('Food', 'FOOD'),
        ('Bills', 'BILLS'),
        ('Travel', 'TRAVEL'),
        ('Healthcare', 'HEALTHCARE'),
        ('Entertainment', 'ENTERTAINMENT'),
        ('Other', 'OTHER'),
    )

    user = models.CharField('Username', max_length=50)
    date = models.DateField('Date')
    amount = models.IntegerField('Amount Spent', default=0)
    category = models.CharField('Category', choices=category_choices, max_length=50)
    currency = models.CharField('Currency', choices=currency_choices, max_length=3)
    note = models.CharField('Transaction Note', max_length=200)
    label = models.CharField('Label', max_length=50)
