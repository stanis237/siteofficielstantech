def cart_context(request):
    """
    Provides cart summary (items count and subtotal) to all templates.
    """
    cart = request.session.get('cart', {})
    total_items = 0
    total_price = 0.0

    for item_id, item in cart.items():
        qty = item.get('quantity', 1)
        price = float(item.get('price', 0))
        total_items += qty
        total_price += qty * price

    return {
        'cart_count': total_items,
        'cart_total': total_price,
        'cart_items': cart,
    }
