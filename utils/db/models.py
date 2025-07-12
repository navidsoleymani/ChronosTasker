from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    """
    Abstract base model that provides:
    - Automatic timestamp fields for creation and updates.
    - Historical tracking via django-simple-history.
    """

    # Timestamp indicating when the object was created
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True,
    )

    # Timestamp indicating the last time the object was updated
    updated_at = models.DateTimeField(
        verbose_name=_('Updated At'),
        auto_now=True,
    )

    # Enables history tracking of model changes (auditing)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True  # Prevents Django from creating a separate table for this model

    def __str__(self):
        """
        Return the string representation of the model instance.
        Defaults to the object's ID.
        """
        return str(self.id)
