# product/utils.py

def compute_trending_score(sales_count, views_count, weight_sales=0.7, weight_views=0.3):
    """
    Compute the trending score based on weighted sales and view counts.
    """
    return (sales_count * weight_sales) + (views_count * weight_views)


def aggregate_order_info(product):
    """
    Calculate aggregated order info for a product.
    For example: total revenue (price * sales_count) and total orders (sales_count).
    """
    return {
        'total_revenue': product.sales_count * float(product.price),
        'total_orders': product.sales_count,
    }
