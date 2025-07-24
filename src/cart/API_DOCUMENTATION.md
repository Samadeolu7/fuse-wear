# Cart API Documentation

This document provides detailed information about the Cart API endpoints and how to interact with them from the frontend.

## Authentication

All cart endpoints require JWT authentication. Include the JWT token in the Authorization header:

```http
Authorization: Bearer your_jwt_token
```

## Data Structures

### Cart Item Request Format

When adding items to cart, use this format:

```json
{
  "product_id": 1,
  "quantity": 1,
  "selected_color": "Red",  // Optional
  "selected_size": "L"      // Optional
}
```

### Cart Item Response Format

The API will return cart items in this format:

```json
{
  "id": 1,
  "cartItemId": "1",
  "name": "Product Name",
  "price": "99.99",
  "description": "Product description",
  "category": "Category name",
  "tags": [
    {
      "id": 1,
      "name": "tag_name",
      "value": "tag_value"
    }
  ],
  "images": [
    {
      "id": 1,
      "image": "image_url",
      "media_type": "image/jpeg",
      "alt_text": "Image description",
      "is_primary": true
    }
  ],
  "quantity": 1,
  "selectedColor": "Red",
  "selectedSize": "L",
  "current_stock": 50,
  "created_at": "2025-07-24T10:00:00Z",
  "updated_at": "2025-07-24T10:00:00Z"
}
```

## Common Error Responses

1. Product Not Found:
```json
{
  "product_id": ["Product not found"]
}
```

2. Insufficient Stock:
```json
{
  "quantity": ["Only X items available"]
}
```

## Interactive API Documentation

For interactive API documentation and testing:

1. Visit `/api/schema/swagger-ui/` in your browser when the server is running
2. You can test endpoints directly and see all available operations
3. The Swagger UI provides example requests and responses

## Best Practices

1. Always check the `current_stock` field in the response to update UI accordingly
2. Handle empty strings for `selectedColor` and `selectedSize` - they indicate no selection
3. Use the `cartItemId` field for cart operations (it's provided as a string to maintain consistency)
4. Cache the product images array but check for updates using the `updated_at` timestamp

## Error Handling

The API uses HTTP status codes:
- 200: Successful operation
- 400: Bad request (check response body for details)
- 401: Unauthorized (invalid/expired token)
- 404: Resource not found
- 500: Server error

Always wrap API calls in try-catch blocks and handle these status codes appropriately in your frontend application.

## Sample Usage (JavaScript/TypeScript)

```typescript
// Add to cart
const addToCart = async (productId: number, quantity: number, color?: string, size?: string) => {
  const response = await fetch('/api/cart/items/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      product_id: productId,
      quantity,
      selected_color: color || '',
      selected_size: size || '',
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    // Handle specific error cases
    if (error.quantity) {
      // Handle stock limitation
    }
    if (error.product_id) {
      // Handle product not found
    }
    throw new Error('Failed to add to cart');
  }

  return response.json();
};
```

## Need Help?

If you encounter any issues or need clarification:
1. Check the Swagger documentation at `/api/schema/swagger-ui/`
2. Refer to the error responses in your API calls
3. Contact the backend team for specific questions

Remember to always validate the API responses in your frontend application and provide appropriate feedback to users.
