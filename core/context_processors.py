def cart_context(request):
    """
    Provides cart summary (items count and subtotal) to all templates.
    """
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
        
    total_items = 0
    total_price = 0.0

    for item_id, item in cart.items():
        if isinstance(item, dict):
            try:
                qty = int(item.get('quantity', 1))
                price = float(item.get('price', 0.0))
                total_items += qty
                total_price += qty * price
            except (ValueError, TypeError):
                continue

    return {
        'cart_count': total_items,
        'cart_total': total_price,
        'cart_items': cart,
    }
