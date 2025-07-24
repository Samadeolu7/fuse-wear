# Cart API Documentation

This document provides detailed information about the Cart API endpoints and how to interact with them from the frontend.

## Base URL

All endpoints are prefixed with `/api/cart/`

## Authentication

All cart endpoints require JWT authentication. Include the JWT token in the Authorization header:

```http
Authorization: Bearer your_jwt_token
```

If the token is missing or invalid, you'll receive a 401 Unauthorized response.

## Endpoints

### 1. Get Cart Items

```http
GET /api/cart/
```

Returns all items in the user's cart.

Response format:
```json
[
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
]
```

### 2. Add Item to Cart

```http
POST /api/cart/add_item/
```

Request body:
```json
{
  "product_id": 1,
  "quantity": 1,
  "selected_color": "Red",  // Optional
  "selected_size": "L"      // Optional
}
```

Success Response (201 Created):
```json
{
  "id": 1,
  "cartItemId": "1",
  "name": "Product Name",
  // ... same format as GET response
}
```

Error Responses:
- Duplicate Item (400 Bad Request):
```json
{
  "message": "This item with the same color/size combination already exists in your cart",
  "error": "duplicate_item"
}
```
- Product Not Found (400 Bad Request):
```json
{
  "product_id": ["Product not found"]
}
```
- Insufficient Stock (400 Bad Request):
```json
{
  "quantity": ["Only X items available"]
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

### 3. Update Cart Item

```http
POST /api/cart/update_item/
```

Request body:
```json
{
  "id": 1,           // Required: Cart item ID
  "quantity": 2,     // Optional: New quantity
  "selected_color": "Blue",  // Optional: New color
  "selected_size": "XL"     // Optional: New size
}
```

Success Response (200 OK):
```json
{
  "id": 1,
  "cartItemId": "1",
  "name": "Product Name",
  // ... same format as GET response
}
```

Error Responses:
- Item Not Found (404 Not Found):
```json
{
  "message": "Item not found in cart",
  "error": "item_not_found"
}
```
- Invalid Quantity (400 Bad Request):
```json
{
  "quantity": ["Only X items available"]
}
```

### 4. Remove Item from Cart

```http
POST /api/cart/remove_item/
```

Request body:
```json
{
  "id": 1  // Cart item ID to remove
}
```

Success Response (204 No Content)

Error Response:
- Item Not Found (404 Not Found):
```json
{
  "message": "Item not found in cart",
  "error": "item_not_found"
}
```

### 5. Clear Cart

```http
POST /api/cart/clear/
```

Removes all items from the cart. No request body needed.

Success Response (204 No Content)

## Sample Usage (TypeScript)

```typescript
interface CartService {
  // Get all cart items
  getCart = async () => {
    const response = await fetch('/api/cart/', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) throw new Error('Failed to fetch cart');
    return response.json();
  };

  // Add item to cart
  addToCart = async ({ product_id, quantity, selected_color, selected_size }) => {
    const response = await fetch('/api/cart/add_item/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        product_id,
        quantity,
        selected_color,
        selected_size,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      if (error.error === 'duplicate_item') {
        throw new Error('Item already in cart');
      }
      throw new Error(error.message || 'Failed to add item');
    }

    return response.json();
  };

  // Update cart item
  updateCartItem = async (id: number, updates: any) => {
    const response = await fetch('/api/cart/update_item/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id, ...updates }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to update item');
    }

    return response.json();
  };

  // Remove item from cart
  removeFromCart = async (id: number) => {
    const response = await fetch('/api/cart/remove_item/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to remove item');
    }
  };

  // Clear cart
  clearCart = async () => {
    const response = await fetch('/api/cart/clear/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to clear cart');
    }
  };
}
```

## Error Handling Best Practices

1. Always check response status codes:
   - 200: Success
   - 201: Created (for add_item)
   - 204: Success, no content (for remove/clear)
   - 400: Bad request (validation errors)
   - 401: Unauthorized (invalid/expired token)
   - 404: Not found (item doesn't exist)

2. Handle specific error types:
   - `duplicate_item`: Item already exists in cart
   - `item_not_found`: Cart item doesn't exist
   - `server_error`: Generic server error

3. Implement retry logic for network failures
4. Show appropriate user feedback for each error type

## Stock Management

1. Always check `current_stock` in the response to update UI
2. Disable "Add to Cart" when quantity would exceed stock
3. Show stock status in the UI (e.g., "Only X items left")
4. Handle out-of-stock scenarios gracefully

## Data Caching Recommendations

1. Cache cart items locally for faster UI updates
2. Invalidate cache on:
   - Adding/removing items
   - Updating quantities
   - Cart cleared
   - Session expired
3. Use `updated_at` timestamp to check for changes

## Need Help?

1. Check the Swagger UI at `/api/schema/swagger-ui/` for interactive testing
2. Use the provided TypeScript code as a starting point
3. Monitor network requests in browser dev tools for debugging
4. Contact the backend team if you encounter unexpected behavior

Remember: Always handle errors gracefully and provide clear feedback to users!
