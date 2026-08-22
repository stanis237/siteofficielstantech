from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json

from .models import Category, Service, Realization, Product, Order, OrderItem, ContactMessage, Application

def get_sanitized_cart(request):
    """
    Safely retrieves and sanitizes the cart dict from the user session.
    Prevents errors from old/incompatible cart data stored in existing cookies.
    """
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    
    sanitized = {}
    for product_id, item in cart.items():
        if isinstance(item, dict):
            try:
                sanitized[str(product_id)] = {
                    'name': str(item.get('name', '')),
                    'price': float(item.get('price', 0.0)),
                    'quantity': max(1, int(item.get('quantity', 1))),
                    'image_url': str(item.get('image_url', '')),
                    'slug': str(item.get('slug', '')),
                }
            except (TypeError, ValueError):
                continue
    return sanitized

def index(request):
    featured_services = Service.objects.filter(is_active=True, is_featured=True)[:3]
    all_services = Service.objects.filter(is_active=True)[:6]
    featured_realizations = Realization.objects.filter(is_active=True, is_featured=True)[:3]
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:4]
    featured_applications = Application.objects.filter(is_active=True, is_featured=True)[:3]

    context = {
        'featured_services': featured_services,
        'all_services': all_services,
        'featured_realizations': featured_realizations,
        'featured_products': featured_products,
        'featured_applications': featured_applications,
    }
    return render(request, 'core/index.html', context)


def services_view(request):
    services = Service.objects.filter(is_active=True)
    categories = Category.objects.filter(type='service')
    context = {
        'services': services,
        'categories': categories,
    }
    return render(request, 'core/services.html', context)


def realisations_view(request):
    realizations = Realization.objects.filter(is_active=True)
    categories = Category.objects.filter(type='realization')
    context = {
        'realizations': realizations,
        'categories': categories,
    }
    return render(request, 'core/realisations.html', context)


def applications_view(request):
    applications = Application.objects.filter(is_active=True)
    categories = Category.objects.filter(type='application')

    cat_slug = request.GET.get('category')
    platform_filter = request.GET.get('platform')

    if cat_slug:
        applications = applications.filter(category__slug=cat_slug)
    if platform_filter:
        applications = applications.filter(platform=platform_filter)

    context = {
        'applications': applications,
        'categories': categories,
        'selected_category': cat_slug,
        'selected_platform': platform_filter,
        'platform_choices': Application.PLATFORM_CHOICES,
    }
    return render(request, 'core/applications.html', context)


def boutique_view(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(type='product')
    
    # Filter by category if requested
    cat_slug = request.GET.get('category')
    if cat_slug:
        products = products.filter(category__slug=cat_slug)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': cat_slug,
    }
    return render(request, 'core/boutique.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'core/product_detail.html', context)


def cart_view(request):
    cart = get_sanitized_cart(request)
    cart_items_detailed = []
    total_amount = 0

    for product_id, item in cart.items():
        try:
            prod = Product.objects.get(id=product_id)
            subtotal = float(item['price']) * item['quantity']
            total_amount += subtotal
            cart_items_detailed.append({
                'product': prod,
                'quantity': item['quantity'],
                'price': item['price'],
                'subtotal': subtotal,
            })
        except (Product.DoesNotExist, ValueError):
            continue

    context = {
        'cart_items_detailed': cart_items_detailed,
        'total_amount': total_amount,
    }
    return render(request, 'core/cart.html', context)


def about_view(request):
    return render(request, 'core/about.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', 'Demande d\'information')
        service_interest = request.POST.get('service_interest', '')
        message_text = request.POST.get('message')

        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                service_interest=service_interest,
                message=message_text
            )
            messages.success(request, "Votre message a été transmis avec succès ! Notre équipe STANTECH vous répondra très rapidement.")
            return redirect('contact')
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")

    return render(request, 'core/contact.html')


# ==========================================
# REST / JSON API ENDPOINTS
# ==========================================

@csrf_exempt
@require_POST
def api_cart_add(request):
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        quantity = int(data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id, is_active=True)

        cart = get_sanitized_cart(request)

        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id] = {
                'name': product.name,
                'price': float(product.current_price),
                'quantity': quantity,
                'image_url': product.image_url,
                'slug': product.slug,
            }

        request.session['cart'] = cart
        request.session.modified = True

        total_items = sum(item['quantity'] for item in cart.values())
        total_price = sum(item['quantity'] * float(item['price']) for item in cart.values())

        return JsonResponse({
            'success': True,
            'message': f"{product.name} a été ajouté au panier !",
            'cart_count': total_items,
            'cart_total': total_price,
            'cart_items': cart,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_POST
def api_cart_update(request):
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        quantity = int(data.get('quantity', 1))

        cart = get_sanitized_cart(request)

        if product_id in cart:
            if quantity > 0:
                cart[product_id]['quantity'] = quantity
            else:
                del cart[product_id]

        request.session['cart'] = cart
        request.session.modified = True

        total_items = sum(item['quantity'] for item in cart.values())
        total_price = sum(item['quantity'] * float(item['price']) for item in cart.values())

        return JsonResponse({
            'success': True,
            'cart_count': total_items,
            'cart_total': total_price,
            'cart_items': cart,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def api_product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = {
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'price': float(product.current_price),
        'short_description': product.short_description,
        'image_url': product.image_url,
        'category_name': product.category.name if product.category else 'Général',
        'specs': product.specs,
    }
    return JsonResponse(data)


@csrf_exempt
@require_POST
def api_checkout(request):
    try:
        data = json.loads(request.body)
        cart = get_sanitized_cart(request)

        if not cart:
            return JsonResponse({'success': False, 'message': 'Votre panier est vide.'}, status=400)

        name = data.get('customer_name')
        email = data.get('customer_email')
        phone = data.get('customer_phone')
        address = data.get('delivery_address')
        city = data.get('city', 'Abidjan')
        notes = data.get('notes', '')

        if not name or not phone or not address:
            return JsonResponse({'success': False, 'message': 'Veuillez remplir le nom, téléphone et l\'adresse.'}, status=400)

        total_amount = sum(item['quantity'] * float(item['price']) for item in cart.values())

        # Create Order
        order = Order.objects.create(
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            delivery_address=address,
            city=city,
            total_amount=total_amount,
            notes=notes,
            status='pending'
        )

        # Create Order Items
        for p_id, item in cart.items():
            product_obj = Product.objects.filter(id=p_id).first()
            OrderItem.objects.create(
                order=order,
                product=product_obj,
                product_name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
                subtotal=item['quantity'] * float(item['price'])
            )

        # Clear Cart in Session
        request.session['cart'] = {}
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'message': 'Commande enregistrée avec succès !',
            'cart_count': 0,
            'cart_total': 0.0,
            'cart_items': {}
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def api_track_order(request):
    """Permet de suivre une commande via son numéro."""
    order_num = request.GET.get('order_number', '').strip().upper()
    if not order_num:
        return JsonResponse({'success': False, 'message': 'Veuillez fournir un numéro de commande.'}, status=400)

    try:
        order = Order.objects.get(order_number=order_num)
        status_labels = {
            'pending': 'En attente de validation',
            'confirmed': 'Commande confirmée / En préparation',
            'shipped': 'Expédiée / En cours de livraison',
            'delivered': 'Livrée avec succès',
            'cancelled': 'Commande annulée'
        }
        
        # Timeline progression
        progress = {
            'pending': 25,
            'confirmed': 50,
            'shipped': 75,
            'delivered': 100,
            'cancelled': 0
        }

        items = [{'name': item.product_name, 'qty': item.quantity} for item in order.items.all()]

        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'status': order.status,
            'status_label': status_labels.get(order.status, order.status),
            'progress': progress.get(order.status, 0),
            'customer_name': order.customer_name,
            'date': order.created_at.strftime('%d/%m/%Y %H:%M'),
            'total': float(order.total_amount),
            'items': items,
        })
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Aucune commande trouvée pour ce numéro.'}, status=404)


def sitemap_xml(request):
    """Génère le fichier XML Sitemap dynamique pour l'indexation des moteurs de recherche."""
    from django.http import HttpResponse
    domain = f"{request.scheme}://{request.get_host()}"
    
    static_pages = [
        {'loc': f"{domain}/", 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': f"{domain}/services/", 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': f"{domain}/realisations/", 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': f"{domain}/boutique/", 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': f"{domain}/a-propos/", 'priority': '0.6', 'changefreq': 'monthly'},
        {'loc': f"{domain}/contact/", 'priority': '0.7', 'changefreq': 'monthly'},
    ]

    products = Product.objects.filter(is_active=True)
    product_urls = []
    for p in products:
        product_urls.append({
            'loc': f"{domain}/boutique/produit/{p.slug}/",
            'lastmod': p.created_at.strftime('%Y-%m-%d'),
            'priority': '0.8',
            'changefreq': 'weekly'
        })

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in static_pages:
        xml_content += f'  <url>\n    <loc>{page["loc"]}</loc>\n    <changefreq>{page["changefreq"]}</changefreq>\n    <priority>{page["priority"]}</priority>\n  </url>\n'

    for prod in product_urls:
        xml_content += f'  <url>\n    <loc>{prod["loc"]}</loc>\n    <lastmod>{prod["lastmod"]}</lastmod>\n    <changefreq>{prod["changefreq"]}</changefreq>\n    <priority>{prod["priority"]}</priority>\n  </url>\n'

    xml_content += '</urlset>'

    return HttpResponse(xml_content, content_type='application/xml')


def robots_txt(request):
    """Génère le fichier robots.txt d'instructions pour les moteurs de recherche."""
    from django.http import HttpResponse
    domain = f"{request.scheme}://{request.get_host()}"
    content = f"""User-agent: *
Disallow: /dashboard/
Disallow: /admin/
Disallow: /api/

Sitemap: {domain}/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')

