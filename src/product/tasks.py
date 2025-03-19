# product/tasks.py

from celery import shared_task
from .models import Product
from .utils import compute_trending_score

@shared_task
def update_trending_scores():
    """
    Task to update trending_score for all products.
    This can be scheduled periodically (e.g., every 5 minutes) via Celery beat.
    """
    weight_sales = 0.7
    weight_views = 0.3
    products = Product.objects.all()
    for product in products:
        new_score = compute_trending_score(product.sales_count, product.views_count, weight_sales, weight_views)
        # Update only the trending_score field to avoid unnecessary writes
        product.trending_score = new_score
        product.save(update_fields=['trending_score'])
