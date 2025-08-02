import React, { useState, useEffect } from 'react';
import api from '../api/axios.js';

const TestConnection = () => {
  const [status, setStatus] = useState('Testing connection...');
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    testConnection();
  }, []);

  const testConnection = async () => {
    setLoading(true);
    setError(null);
    
    try {
      setStatus('🔄 Testing backend connection...');
      
      // Test Products API
      const productsResponse = await api.get('/products/products/');
      const productsData = productsResponse.data.results || productsResponse.data || [];
      setProducts(productsData);
      
      // Test Categories API
      const categoriesResponse = await api.get('/products/categories/');
      const categoriesData = categoriesResponse.data.results || categoriesResponse.data || [];
      setCategories(categoriesData);
      
      setStatus('✅ Backend connection successful!');
      
    } catch (error) {
      setStatus('❌ Backend connection failed');
      setError(error.response?.data?.detail || error.message);
      console.error('Connection error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h1 className="text-3xl font-bold mb-6 text-gray-900">🔧 API Connection Test</h1>
          
          <div className="mb-6">
            <div className="flex items-center mb-4">
              {loading && (
                <svg className="animate-spin h-5 w-5 mr-3 text-blue-600" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              )}
              <p className="text-lg font-medium">{status}</p>
            </div>
            
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                <strong>Error:</strong> {error}
              </div>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* API Endpoints Status */}
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-3">📡 API Endpoints</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Products API:</span>
                  <span className={products.length > 0 ? 'text-green-600' : 'text-red-600'}>
                    {products.length > 0 ? '✅ Working' : '❌ Failed'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Categories API:</span>
                  <span className={categories.length > 0 ? 'text-green-600' : 'text-red-600'}>
                    {categories.length > 0 ? '✅ Working' : '❌ Failed'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Products Count:</span>
                  <span className="font-medium">{products.length}</span>
                </div>
                <div className="flex justify-between">
                  <span>Categories Count:</span>
                  <span className="font-medium">{categories.length}</span>
                </div>
              </div>
            </div>

            {/* Connection Info */}
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-blue-900 mb-3">🌐 Connection Info</h3>
              <div className="space-y-2 text-sm text-blue-800">
                <div>
                  <strong>Frontend:</strong> {window.location.origin}
                </div>
                <div>
                  <strong>Backend API:</strong> {import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}
                </div>
                <div>
                  <strong>Environment:</strong> {import.meta.env.MODE}
                </div>
              </div>
            </div>
          </div>

          <button 
            onClick={testConnection}
            disabled={loading}
            className="mt-6 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
          >
            {loading ? 'Testing...' : 'Test Again'}
          </button>
        </div>

        {/* Sample Data Display */}
        {(products.length > 0 || categories.length > 0) && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Sample Products */}
            {products.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-900">🛍️ Sample Products</h2>
                <div className="space-y-3">
                  {products.slice(0, 5).map((product, index) => (
                    <div key={product.id || index} className="p-3 bg-gray-50 rounded-lg border">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-medium text-gray-900">{product.name || 'Sample Product'}</p>
                          <p className="text-sm text-gray-600 mt-1">{product.description || 'No description'}</p>
                          <p className="text-xs text-gray-500 mt-1">Category: {product.category_name || 'N/A'}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-lg font-bold text-blue-600">${product.price || '0.00'}</p>
                          <p className="text-xs text-gray-500">Stock: {product.stock_quantity || 0}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Sample Categories */}
            {categories.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-900">📂 Categories</h2>
                <div className="space-y-3">
                  {categories.map((category, index) => (
                    <div key={category.id || index} className="p-3 bg-gray-50 rounded-lg border">
                      <p className="font-medium text-gray-900">{category.name || 'Sample Category'}</p>
                      <p className="text-sm text-gray-600 mt-1">{category.description || 'No description'}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Quick Navigation */}
        <div className="mt-6 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-900">🚀 Quick Navigation</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <a href="/" className="bg-blue-100 hover:bg-blue-200 text-blue-800 p-3 rounded-lg text-center transition-colors">
              🏠 Home
            </a>
            <a href="/products" className="bg-green-100 hover:bg-green-200 text-green-800 p-3 rounded-lg text-center transition-colors">
              🛍️ Products
            </a>
            <a href="/login" className="bg-purple-100 hover:bg-purple-200 text-purple-800 p-3 rounded-lg text-center transition-colors">
              🔐 Login
            </a>
            <a href="/register" className="bg-orange-100 hover:bg-orange-200 text-orange-800 p-3 rounded-lg text-center transition-colors">
              📝 Register
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TestConnection;