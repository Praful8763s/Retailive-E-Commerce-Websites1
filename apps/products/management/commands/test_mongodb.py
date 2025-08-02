from django.core.management.base import BaseCommand
from django.conf import settings
import pymongo
import os

class Command(BaseCommand):
    help = 'Test MongoDB connection'

    def handle(self, *args, **options):
        self.stdout.write('Testing MongoDB connection...')
        
        try:
            # Get MongoDB URI from settings
            mongo_uri = os.getenv('MONGO_URI', 'mongodb+srv://prafulsonwane58:rqsnNGrMRBtHS1Sx@cluster0.mcove5d.mongodb.net/retailhive')
            
            # Create MongoDB client
            client = pymongo.MongoClient(mongo_uri)
            
            # Test connection
            client.admin.command('ping')
            
            # Get database
            db = client['retailhive']
            
            # List collections
            collections = db.list_collection_names()
            
            self.stdout.write(
                self.style.SUCCESS('✅ MongoDB connection successful!')
            )
            self.stdout.write(f'📊 Database: retailhive')
            self.stdout.write(f'📁 Collections: {collections if collections else "No collections yet"}')
            
            # Test write operation
            test_collection = db['connection_test']
            test_doc = {'test': True, 'message': 'Connection successful'}
            result = test_collection.insert_one(test_doc)
            
            self.stdout.write(f'✅ Test document inserted with ID: {result.inserted_id}')
            
            # Clean up test document
            test_collection.delete_one({'_id': result.inserted_id})
            self.stdout.write('🧹 Test document cleaned up')
            
            client.close()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ MongoDB connection failed: {str(e)}')
            )
            self.stdout.write('Please check your MongoDB URI and network connection.')