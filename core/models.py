import uuid
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    CATEGORY_TYPES = [
        ('product', 'Boutique (Produits)'),
        ('service', 'Services Entreprise'),
        ('realization', 'Réalisations & Projets'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug (URL)")
    type = models.CharField(max_length=20, choices=CATEGORY_TYPES, default='product', verbose_name="Type de contenu")
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, default="folder", help_text="Nom de l'icône Lucide (ex: cpu, shield, server, shopping-bag)")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['type', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre du Service")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug (URL)")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'type': 'service'}, verbose_name="Catégorie")
    icon = models.CharField(max_length=50, default="cpu", help_text="Icône Lucide (ex: cpu, shield, code, database, cloud, settings)")
    short_description = models.TextField(verbose_name="Résumé court")
    full_description = models.TextField(blank=True, verbose_name="Description complète")
    features = models.TextField(blank=True, help_text="Une fonctionnalité par ligne", verbose_name="Points clés / Inclus")
    image_url = models.CharField(max_length=500, blank=True, verbose_name="URL ou chemin de l'image")
    is_featured = models.BooleanField(default=False, verbose_name="Mettre en avant (Page d'accueil)")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_features_list(self):
        if not self.features:
            return []
        return [f.strip() for f in self.features.split('\n') if f.strip()]

    def __str__(self):
        return self.title


class Realization(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre du projet / Réalisation")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug (URL)")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'type': 'realization'}, verbose_name="Domaine d'intervention")
    client_name = models.CharField(max_length=150, blank=True, verbose_name="Nom du client")
    short_description = models.TextField(verbose_name="Résumé court")
    full_description = models.TextField(blank=True, verbose_name="Description détaillée")
    tech_stack = models.CharField(max_length=255, blank=True, verbose_name="Technologies utilisées (séparées par des virgules)")
    image_url = models.CharField(max_length=500, blank=True, verbose_name="URL de l'image de présentation")
    completion_date = models.DateField(null=True, blank=True, verbose_name="Date de livraison")
    project_url = models.URLField(blank=True, verbose_name="Lien externe du projet")
    is_featured = models.BooleanField(default=False, verbose_name="Mettre en vedette (Accueil)")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        verbose_name = "Réalisation"
        verbose_name_plural = "Réalisations"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_tech_tags(self):
        if not self.tech_stack:
            return []
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug (URL)")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'type': 'product'}, verbose_name="Catégorie")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (FCFA / EUR)")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix réduit (Optionnel)")
    short_description = models.TextField(verbose_name="Courte description")
    full_description = models.TextField(blank=True, verbose_name="Description complète & Spécifications")
    stock = models.IntegerField(default=10, verbose_name="Quantité en stock")
    badge = models.CharField(max_length=50, blank=True, help_text="ex: Nouveau, Promo, Top Ventes, Recommandé", verbose_name="Badge / Label")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name="Note sur 5")
    reviews_count = models.IntegerField(default=12, verbose_name="Nombre d'avis")
    image_url = models.CharField(max_length=500, blank=True, verbose_name="URL de l'image du produit")
    specs = models.TextField(blank=True, help_text="Spécifications (ex: Garantie: 2 ans\\nMarque: STANTECH)", verbose_name="Fiche technique (Clé: Valeur par ligne)")
    is_featured = models.BooleanField(default=False, verbose_name="Produit Vedette (En avant)")
    is_active = models.BooleanField(default=True, verbose_name="En vente / Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        verbose_name = "Produit (Boutique)"
        verbose_name_plural = "Produits (Boutique)"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def current_price(self):
        return self.discount_price if self.discount_price and self.discount_price > 0 else self.price

    def get_specs_dict(self):
        specs_list = []
        if self.specs:
            for line in self.specs.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    specs_list.append({'key': key.strip(), 'value': val.strip()})
        return specs_list

    def __str__(self):
        return f"{self.name} - {self.price} FCFA"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('shipped', 'Expédiée / En livraison'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]

    order_number = models.CharField(max_length=50, unique=True, editable=False, verbose_name="Numéro de Commande")
    customer_name = models.CharField(max_length=150, verbose_name="Nom complet du client")
    customer_email = models.EmailField(verbose_name="Adresse email")
    customer_phone = models.CharField(max_length=30, verbose_name="Numéro de téléphone")
    delivery_address = models.TextField(verbose_name="Adresse de livraison")
    city = models.CharField(max_length=100, default="Abidjan / Paris", verbose_name="Ville")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Montant total")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut de la commande")
    notes = models.TextField(blank=True, verbose_name="Notes / Instructions de livraison")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de commande")

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ST-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande {self.order_number} - {self.customer_name} ({self.get_status_display()})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Commande")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Produit")
    product_name = models.CharField(max_length=200, verbose_name="Nom du produit")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    quantity = models.IntegerField(default=1, verbose_name="Quantité")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sous-total")

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Téléphone")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    service_interest = models.CharField(max_length=100, blank=True, verbose_name="Service concerné")
    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(default=False, verbose_name="Lu / Traité")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")

    class Meta:
        verbose_name = "Message de Contact"
        verbose_name_plural = "Messages de Contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"Message de {self.name} - {self.subject}"
