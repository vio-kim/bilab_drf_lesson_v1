from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import AbstractUUID, AbstractTimeTracker
from utils.const import PhoneCompanyChoice, PhoneColorChoice


class Phone(AbstractUUID, AbstractTimeTracker):
    company = models.CharField(
        choices=PhoneCompanyChoice.choices,
        default=PhoneCompanyChoice.OTHER.value,
        max_length=255,
        verbose_name=_('Company')
    )
    model = models.CharField(
        max_length=255,
        verbose_name=_('Model')
    )
    color = models.CharField(
        choices=PhoneColorChoice.choices,
        default=PhoneColorChoice.NO_COLOR.value,
        max_length=255,
        verbose_name=_('Color')
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Price')
    )
    description = models.CharField(
        max_length=1000,
        verbose_name=_('Description')
    )
    memory = models.ForeignKey(
        'products.Memory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Memory'),
        related_name='phones'
    )

    class Meta:
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'

    def __str__(self):
        return f'{self.company}, {self.model}, {self.memory}'
