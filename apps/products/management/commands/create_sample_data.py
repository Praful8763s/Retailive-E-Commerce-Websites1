from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.products.models import Category, Product

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and literature'},
            {'name': 'Home & Garden', 'description': 'Home improvement and gardening'},
            {'name': 'Sports', 'description': 'Sports and fitness equipment'},
        ]
        
        categories = []
        for cat_data in categories_data:
            try:
                category, created = Category.objects.get_or_create(
                    name=cat_data['name'],
                    defaults={'description': cat_data['description']}
                )
                categories.append(category)
                if created:
                    self.stdout.write(f'✅ Created category: {category.name}')
                else:
                    self.stdout.write(f'✅ Category {category.name} already exists')
            except Exception as e:
                self.stdout.write(f'⚠️ Category {cat_data["name"]} creation skipped: {e}')
        
        # Create products
        products_data = [
            {
                'name': 'Smartphone',
                'description': 'Latest smartphone with advanced features',
                'price': 699.99,
                'stock_quantity': 50,
                'image': 'https://via.placeholder.com/300x300?text=Smartphone'
            },
            {
                'name': 'Laptop',
                'description': 'High-performance laptop for work and gaming',
                'price': 1299.99,
                'stock_quantity': 25,
                'image': 'https://via.placeholder.com/300x300?text=Laptop'
            },
            {
                'name': 'T-Shirt',
                'description': 'Comfortable cotton t-shirt',
                'price': 19.99,
                'stock_quantity': 100,
                'image': 'https://via.placeholder.com/300x300?text=T-Shirt'
            },
            {
                'name': 'Jeans',
                'description': 'Classic blue jeans',
                'price': 49.99,
                'stock_quantity': 75,
                'image': 'https://via.placeholder.com/300x300?text=Jeans'
            },
            {
                'name': 'Programming Book',
                'description': 'Learn programming with this comprehensive guide',
                'price': 39.99,
                'stock_quantity': 30,
                'image': 'https://via.placeholder.com/300x300?text=Book'
            },
            {
                'name': 'Coffee Maker',
                'description': 'Automatic coffee maker for your kitchen',
                'price': 89.99,
                'stock_quantity': 20,
                'image': 'https://via.placeholder.com/300x300?text=Coffee+Maker'
            },
            {
                'name': 'Running Shoes',
                'description': 'Comfortable running shoes for athletes',
                'price': 79.99,
                'stock_quantity': 60,
                'image': 'https://via.placeholder.com/300x300?text=Running+Shoes'
            },
            {
                'name': 'Yoga Mat',
                'description': 'Non-slip yoga mat for exercise',
                'price': 24.99,
                'stock_quantity': 40,
                'image': 'https://via.placeholder.com/300x300?text=Yoga+Mat'
            },
        ]
        
        # Create products with categories
        for i, product_data in enumerate(products_data):
            try:
                if categories:
                    category = categories[i % len(categories)]
                    product_data['category'] = category
                
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults=product_data
                )
                if created:
                    self.stdout.write(f'✅ Created product: {product.name}')
                else:
                    self.stdout.write(f'✅ Product {product.name} already exists')
            except Exception as e:
                self.stdout.write(f'⚠️ Product {product_data["name"]} creation skipped: {e}')
        
        # Create sample users with different roles
        try:
            from django.core.management import call_command
            call_command('create_sample_users')
        except Exception as e:
            self.stdout.write(f'⚠️ User creation skipped: {e}')
        
        # Assign some products to retailers
        try:
            retailer1 = User.objects.get(username='retailer1')
            retailer2 = User.objects.get(username='retailer2')
            
            # Assign products to retailers
            products_to_assign = Product.objects.all()[:4]
            for i, product in enumerate(products_to_assign):
                if i % 2 == 0:
                    product.retailer = retailer1
                else:
                    product.retailer = retailer2
                product.is_approved = True  # Pre-approve some products
                product.save()
                self.stdout.write(f'✅ Assigned {product.name} to {product.retailer.username}')
        except Exception as e:
            self.stdout.write(f'⚠️ Product assignment skipped: {e}')
        
        self.stdout.write(self.style.SUCCESS('✅ Complete sample data created successfully!'))
        self.stdout.write('\n🎯 What you can test:')
        self.stdout.write('👑 Admin Dashboard: Login as admin to approve products')
        self.stdout.write('🏪 Retailer Dashboard: Login as retailer1/retailer2 to manage products')
        self.stdout.write('👤 Customer Experience: Login as customer1/customer2 to shop')
        self.stdout.write('🛒 Shopping Cart: Add products and place orders')
        self.stdout.write('📱 Responsive Design: Test on mobile and desktop')