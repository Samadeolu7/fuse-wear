# product/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .tasks import update_trending_scores
from .utils import aggregate_order_info

@receiver(post_save, sender=Product)
def update_product_fields(sender, instance, created, **kwargs):
    """
    Trigger background updates when a product is saved.
    - Schedule a task to update the trending score.
    - Update aggregated order info without recursion by using queryset update.
    """
    # Schedule trending score update (this task can be optimized to update only when needed)
    update_trending_scores.delay()

    # Update aggregated order info; avoid recursion by using the queryset update.
    info = aggregate_order_info(instance)
    sender.objects.filter(pk=instance.pk).update(aggregated_order_info=info)
