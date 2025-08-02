# 🛍️ RetailHive - Complete Full Stack E-commerce Platform

A modern, full-featured e-commerce platform built with Django REST Framework backend and React frontend, featuring MongoDB database integration and comprehensive API connectivity.

## 🌟 Features

### 🔐 Authentication & User Management
- ✅ User registration and login
- ✅ JWT token-based authentication
- ✅ User profile management
- ✅ Password validation and security

### 🛍️ Product Management
- ✅ Product catalog with categories
- ✅ Product search and filtering
- ✅ Product reviews and ratings
- ✅ Stock management
- ✅ Image support

### 🛒 Shopping Cart & Orders
- ✅ Add/remove items from cart
- ✅ Real-time cart updates
- ✅ Order processing and tracking
- ✅ Order history
- ✅ Email notifications

### 🎨 Frontend Features
- ✅ Responsive design (mobile-friendly)
- ✅ Modern UI with Tailwind CSS
- ✅ Real-time updates
- ✅ Loading states and error handling
- ✅ Smooth navigation

### 🔧 Technical Features
- ✅ MongoDB database integration
- ✅ RESTful API design
- ✅ CORS configuration
- ✅ Environment variable management
- ✅ Error handling and validation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB Atlas account (or local MongoDB)

### 🔥 One-Command Setup
```bash
setup_complete_project.bat
```

### 🏃‍♂️ Running the Application

1. **Start Backend** (Terminal 1):
   ```bash
   start_backend.bat
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   start_frontend.bat
   ```

### 🌐 Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin
- **API Test**: http://localhost:3000/test

## 🏗️ Project Structure

```
RetailHive/
├── backend/                    # Django REST API
│   ├── retailhive/            # Core Django project
│   │   ├── settings.py        # MongoDB & API configuration
│   │   ├── urls.py           # API routing
│   │   └── ...
│   ├── apps/                  # Django applications
│   │   ├── products/         # Product management
│   │   ├── users/            # User authentication
│   │   └── orders/           # Cart & order processing
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment variables
│
├── frontend/                  # React application
│   ├── src/
│   │   ├── api/              # API service functions
│   │   ├── components/       # Reusable UI components
│   │   ├── contexts/         # React Context (Auth, Cart)
│   │   ├── pages/            # Page components
│   │   ├── routes/           # Route definitions
│   │   └── utils/            # Utility functions
│   ├── package.json          # Node.js dependencies
│   └── tailwind.config.js    # Tailwind CSS config
│
└── setup_complete_project.bat # One-command setup
```

## 🔧 API Endpoints

### 🔐 Authentication
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/update/` - Update profile

### 🛍️ Products
- `GET /api/products/products/` - List products
- `GET /api/products/products/{id}/` - Product details
- `GET /api/products/products/search/?q=query` - Search products
- `GET /api/products/categories/` - List categories
- `POST /api/products/products/{id}/add_review/` - Add review

### 🛒 Cart & Orders
- `GET /api/orders/cart/` - Get user cart
- `POST /api/orders/cart/add/` - Add item to cart
- `DELETE /api/orders/cart/remove/{id}/` - Remove from cart
- `GET /api/orders/orders/` - List user orders
- `POST /api/orders/orders/create_order/` - Create order

## 🗄️ Database Configuration

### MongoDB Atlas Setup
The application is configured to use MongoDB Atlas with the following connection:

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'retailhive',
        'CLIENT': {
            'host': 'mongodb+srv://prafulsonwane58:rqsnNGrMRBtHS1Sx@cluster0.mcove5d.mongodb.net/retailhive',
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1',
        }
    }
}
```

## 📧 Email Configuration

Gmail SMTP is configured for order confirmations:

```python
EMAIL_HOST_USER = 'prafulsonwane13@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 👤 Test Credentials

Default test user created during setup:
- **Username**: `testuser`
- **Password**: `testpass123`
- **Email**: `test@example.com`

## 🧪 Testing the Setup

1. Visit http://localhost:3000/test to verify API connectivity
2. Register a new user or login with test credentials
3. Browse products and add items to cart
4. Complete an order to test the full workflow

## 🛠️ Development

### Backend Development
```bash
cd backend
call .venv\Scripts\activate
python manage.py runserver
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Adding Sample Data
```bash
cd backend
python manage.py create_sample_data
```

### Testing MongoDB Connection
```bash
cd backend
python manage.py test_mongodb
```

## 🔒 Security Features

- JWT token authentication
- CORS configuration
- Input validation and sanitization
- SQL injection protection (via Django ORM)
- XSS protection
- CSRF protection

## 📱 Responsive Design

The application is fully responsive and works on:
- 📱 Mobile devices (320px+)
- 📱 Tablets (768px+)
- 💻 Desktop (1024px+)
- 🖥️ Large screens (1280px+)

## 🚀 Deployment Ready

The application is configured for easy deployment with:
- Environment variable management
- Static file handling
- Production-ready settings
- Docker support (optional)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the API test page: http://localhost:3000/test
2. Verify MongoDB connection
3. Check console logs for errors
4. Ensure all dependencies are installed

## 🎉 Success!

Your RetailHive e-commerce platform is now fully operational with:
- ✅ Complete user authentication system
- ✅ Product catalog with search functionality
- ✅ Shopping cart and order processing
- ✅ MongoDB database integration
- ✅ Responsive React frontend
- ✅ RESTful API backend
- ✅ Email notifications
- ✅ Admin panel access

Happy coding! 🚀
