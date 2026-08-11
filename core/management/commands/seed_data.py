from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Category, Service, Realization, Product

class Command(BaseCommand):
    help = 'Populates the database with initial demo data for STANTECH enterprise & boutique'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Create Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@stantech.ci', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created: admin / admin123'))

        # 1. Categories
        cat_services_dev, _ = Category.objects.get_or_create(
            name="Développement & Logiciels",
            type="service",
            defaults={"description": "Conception d'applications web, mobiles et systèmes d'information", "icon": "code"}
        )

        cat_services_infra, _ = Category.objects.get_or_create(
            name="Infrastructure & Cloud",
            type="service",
            defaults={"description": "Architecture serveur, cybersécurité et infogérance", "icon": "cloud"}
        )

        cat_services_iot, _ = Category.objects.get_or_create(
            name="IoT & Systèmes Embarqués",
            type="service",
            defaults={"description": "Solutions d'automatisation, télémétrie et objets connectés", "icon": "cpu"}
        )

        cat_real_telecom, _ = Category.objects.get_or_create(
            name="Télécoms & Réseaux",
            type="realization",
            defaults={"description": "Projets de télécommunications et infrastructures de données", "icon": "wifi"}
        )

        cat_real_industriels, _ = Category.objects.get_or_create(
            name="Projets Industriels",
            type="realization",
            defaults={"description": "Automates et contrôle de procédés industriels", "icon": "settings"}
        )

        cat_prod_hardware, _ = Category.objects.get_or_create(
            name="Matériel & Equipements",
            type="product",
            defaults={"description": "Serveurs, switchs, routeurs et équipements informatiques de pointe", "icon": "server"}
        )

        cat_prod_iot, _ = Category.objects.get_or_create(
            name="Kits & Capteurs IoT",
            type="product",
            defaults={"description": "Capteurs intelligents, hubs et cartes d'acquisition de données", "icon": "cpu"}
        )

        cat_prod_sec, _ = Category.objects.get_or_create(
            name="Sécurité & Surveillance",
            type="product",
            defaults={"description": "Pare-feux matériels, caméras IP et systèmes de contrôle d'accès", "icon": "shield"}
        )

        # 2. Services
        services_data = [
            {
                "title": "Ingénierie Logicielle & Métier",
                "category": cat_services_dev,
                "icon": "code",
                "short_description": "Développement sur-mesure de plateformes web, applications mobiles et API hautes performances.",
                "full_description": "STANTECH conçoit des solutions d'entreprise évolutives avec des architectures microservices, intégrant les dernières avancées technologiques pour automatiser et optimiser vos processus métier.",
                "features": "Architecture Cloud-Native\nApplications Mobiles iOS & Android\nAPI RESTful & GraphQL sécurisées\nOptimisation des performances & bases de données",
                "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80",
                "is_featured": True,
                "order": 1
            },
            {
                "title": "Infrastructure Cloud & Cybersécurité",
                "category": cat_services_infra,
                "icon": "shield",
                "short_description": "Audit de sécurité, protection contre les cyberattaques et migration vers le Cloud hybride.",
                "full_description": "Protégez vos actifs critiques et sécurisez votre réseau grâce à nos audits d'intrusion de pointe, nos pare-feux managés et nos plans de reprise d'activité (PRA) sur mesure.",
                "features": "Audit de vulnérabilité & Test de pénétration\nMigration AWS, Azure & Cloud Privé STANTECH\nProtection Anti-DDoS & Pare-feu applicatif\nSurveillance 24/7 & SOC Managé",
                "image_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1200&q=80",
                "is_featured": True,
                "order": 2
            },
            {
                "title": "IoT & Automatisation Industrielle",
                "category": cat_services_iot,
                "icon": "cpu",
                "short_description": "Solutions globales d'objets connectés, télémétrie en temps réel et automatisation de pointe.",
                "full_description": "Connectez vos installations industrielles et surveillez vos métriques critiques à distance avec nos capteurs intelligents et nos algorithmes d'analyse prédictive.",
                "features": "Capteurs intelligents sans fil (LoRaWAN, NB-IoT)\nTableaux de bord d'analyse en temps réel\nMaintenance prédictive assistée par IA\nIntégration d'automates PLC & SCADA",
                "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
                "is_featured": True,
                "order": 3
            },
            {
                "title": "Transformation Numérique & Consulting",
                "category": cat_services_dev,
                "icon": "trending-up",
                "short_description": "Accompagnement stratégique pour la modernisation technologique des grandes entreprises et PME.",
                "full_description": "Nos experts vous guident dans le choix des technologies émergentes, la gouvernance de vos données et le déploiement de stratégies digitales à fort impact.",
                "features": "Schéma Directeur Informatique (SDI)\nGouvernance des Données & Compliance\nFormation & Conduite du changement\nUrbanisation du système d'information",
                "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
                "is_featured": False,
                "order": 4
            }
        ]

        for s_data in services_data:
            Service.objects.get_or_create(title=s_data["title"], defaults=s_data)

        # 3. Realizations
        realizations_data = [
            {
                "title": "Système IoT Smart Energy & Supervision",
                "category": cat_real_industriels,
                "client_name": "Groupement Industriel Ivoirien",
                "short_description": "Déploiement de 450 capteurs IoT de surveillance énergétique en temps réel sur 5 sites industriels.",
                "full_description": "Mise en place d'une infrastructure complète de collecte de données réseau et d'une plateforme SaaS permettant une réduction de 28% de la consommation d'énergie.",
                "tech_stack": "Python, Django, LoRaWAN, PostgreSQL, Vue.js, Docker",
                "image_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1200&q=80",
                "is_featured": True
            },
            {
                "title": "Plateforme Logistique Portuaire & Fleet Management",
                "category": cat_real_telecom,
                "client_name": "Port Autonome d'Abidjan (Partenaire)",
                "short_description": "Digitalisation complète du suivi des conteneurs et géolocalisation haute précision de la flotte.",
                "full_description": "Solution haute disponibilité gérant plus de 10 000 conteneurs par jour avec notifications instantanées, calcul d'itinéraires et prédiction des retards.",
                "tech_stack": "Django REST Framework, React Native, Redis, WebSockets, GPS",
                "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1200&q=80",
                "is_featured": True
            },
            {
                "title": "Modernisation Datacenter & Cloud Sécurisé",
                "category": cat_real_telecom,
                "client_name": "Banque Internationale de Crédit",
                "short_description": "Interconnexion fibre optique et sécurisation zéro-trust d'un réseau bancaire multi-agences.",
                "full_description": "Architecture réseau redondante avec chiffrement militaire AES-256, migration sans coupure de service et mise en place d'un SOC de supervision.",
                "tech_stack": "Cisco, Fortinet, Kubernetes, Terraform, Cybersecurity",
                "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80",
                "is_featured": True
            }
        ]

        for r_data in realizations_data:
            Realization.objects.get_or_create(title=r_data["title"], defaults=r_data)

        # 4. Products (Boutique)
        products_data = [
            {
                "name": "Serveur STANTECH Enterprise Rack 1U - GenX",
                "category": cat_prod_hardware,
                "price": 1450000,
                "discount_price": 1290000,
                "short_description": "Serveur haute densité bi-processeur conçu pour les charges de travail intensives et la virtualisation.",
                "full_description": "Le STANTECH Enterprise Rack 1U est le choix ultime pour les datacenters exigeants. Équipé de processeurs Intel Xeon Scalable de dernière génération, de mémoire RAM ECC extensible à 512 Go et de baies de stockage SSD NVMe ultra-rapides.",
                "stock": 8,
                "badge": "Top Ventes",
                "rating": 4.9,
                "reviews_count": 24,
                "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80",
                "specs": "Processeur: Dual Intel Xeon Silver 4314\nRAM: 64 Go DDR4 ECC\nStockage: 2x 1TB SSD NVMe Enterprise\nAlimentation: Redondante 750W Gold\nGarantie: 3 Ans sur site STANTECH",
                "is_featured": True
            },
            {
                "name": "Pack Smart IoT Gateway Hub Pro",
                "category": cat_prod_iot,
                "price": 380000,
                "discount_price": 325000,
                "short_description": "Passerelle IoT industrielle multiprotocole (LoRaWAN, Zigbee, Ethernet, 4G LTE).",
                "full_description": "Permet de centraliser et d'acheminer en toute sécurité les métriques de centaines de capteurs environnants vers votre Cloud ou serveur local avec une latence ultra-faible.",
                "stock": 15,
                "badge": "Recommandé",
                "rating": 4.8,
                "reviews_count": 18,
                "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
                "specs": "Protocole: LoRaWAN 868/915MHz, 4G, WiFi 6\nProtection: Boîtier étanche IP67\nPortée: Jusqu'à 15 km en zone dégagée\nAlimentation: PoE ou Solaire",
                "is_featured": True
            },
            {
                "name": "Station de Travail STANTECH Power Station AI",
                "category": cat_prod_hardware,
                "price": 2100000,
                "discount_price": 1950000,
                "short_description": "Workstation ultra-puissante dédiée au Machine Learning, au rendu 3D et à la simulation d'ingénierie.",
                "full_description": "Dotée d'un GPU NVIDIA RTX 4090 24GB et d'un processeur AMD Ryzen Threadripper, cette station offre une puissance de calcul inégalée pour les ingénieurs et chercheurs.",
                "stock": 5,
                "badge": "Nouveau",
                "rating": 5.0,
                "reviews_count": 12,
                "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=800&q=80",
                "specs": "Processeur: AMD Ryzen 9 7950X 16-Core\nCarte Graphique: NVIDIA RTX 4090 24GB GDDR6X\nRAM: 128 Go DDR5 5600MHz\nRefroidissement: Watercooling Custom 360mm",
                "is_featured": True
            },
            {
                "name": "Pare-feu Matériel STANTECH CyberShield S500",
                "category": cat_prod_sec,
                "price": 750000,
                "discount_price": None,
                "short_description": "Appliance de sécurité réseau UTM avec inspection SSL en temps réel et VPN IPSec haute vitesse.",
                "full_description": "Protégez votre réseau d'entreprise contre les ransomwares, les attaques zero-day et le piratage avec le pare-feu CyberShield S500 disposant d'un débit d'inspection de 5 Gbps.",
                "stock": 12,
                "badge": "Sécurité",
                "rating": 4.9,
                "reviews_count": 30,
                "image_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80",
                "specs": "Débit Pare-feu: 5.5 Gbps\nDébit IPSec VPN: 2.1 Gbps\nNombre d'utilisateurs max: 250\nPorts: 8x Gigabit RJ45 + 2x SFP+",
                "is_featured": True
            },
            {
                "name": "Capteur Industriel Télémétrie Température & Humidité",
                "category": cat_prod_iot,
                "price": 65000,
                "discount_price": 55000,
                "short_description": "Capteur LoRaWAN sans fil haute précision pour entrepôts et salles blanches.",
                "full_description": "Conçu pour résister aux environnements extrêmes, ce capteur offre 10 ans d'autonomie sur batterie haute capacité et transmet des alertes automatiques par SMS/Email.",
                "stock": 45,
                "badge": "Promo",
                "rating": 4.7,
                "reviews_count": 42,
                "image_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
                "specs": "Autonomie: 10 ans (batterie LiSOCl2)\nPrécision Température: ±0.2°C\nNorme: IP65 étanche\nCalibration: Usine certifiée ISO",
                "is_featured": False
            },
            {
                "name": "Switch Managé 24 Ports PoE+ STANTECH NetGig",
                "category": cat_prod_hardware,
                "price": 420000,
                "discount_price": None,
                "short_description": "Switch réseau d'entreprise 24 ports Gigabit PoE+ avec 4 uplinks SFP+ 10G.",
                "full_description": "Offrez une alimentation PoE fluide (jusqu'à 370W total) pour vos caméras IP et points d'accès WiFi 6 tout en garantissant un routage de niveau L2+/L3.",
                "stock": 20,
                "badge": "Réseau",
                "rating": 4.8,
                "reviews_count": 15,
                "image_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=800&q=80",
                "specs": "Ports: 24x 10/100/1000 Mbps PoE+ (370W)\nUplinks: 4x 10G SFP+\nCapacité de commutation: 128 Gbps\nManagement: Web UI, CLI, SNMP, Cloud STANTECH",
                "is_featured": False
            }
        ]

        for p_data in products_data:
            Product.objects.get_or_create(name=p_data["name"], defaults=p_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded STANTECH database with high-quality categories, services, realizations, and boutique products!'))
