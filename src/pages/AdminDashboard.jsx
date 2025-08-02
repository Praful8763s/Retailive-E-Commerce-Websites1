import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext.jsx';
import api from '../api/axios.js';
import Button from '../components/Button.jsx';
import Loader from '../components/Loader.jsx';

const AdminDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({});
  const [pendingProducts, setPendingProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (user?.userprofile?.role === 'admin' || user?.is_staff) {
      fetchAdminData();
    }
  }, [user]);

  const fetchAdminData = async () => {
    try {
      setLoading(true);
      const [statsRes, pendingRes] = await Promise.all([
        api.get('/products/admin/products/dashboard_stats/'),
        api.get('/products/admin/products/pending_approval/')
      ]);
      
      setStats(statsRes.data);
      setPendingProducts(pendingRes.data.results || pendingRes.data);
    } catch (error) {
      console.error('Error fetching admin data:', error);
    } finally {
      setLoading(false);
    }
  };

  const approveProduct = async (productId) => {
    try {
      await api.patch(`/products/admin/products/${productId}/approve_product/`);
      alert('Product approved successfully!');
      fetchAdminData(); // Refresh data
    } catch (error) {
      alert('Failed to approve product');
    }
  };

  const rejectProduct = async (productId, reason = '') => {
    try {
      await api.patch(`/products/admin/products/${productId}/reject_product/`, {
        reason: reason
      });
      alert('Product rejected successfully!');
      fetchAdminData(); // Refresh data
    } catch (error) {
      alert('Failed to reject product');
    }
  };

  const bulkApprove = async (productIds) => {
    try {
      await api.patch('/products/admin/products/bulk_approve/', {
        product_ids: productIds
      });
      alert('Products approved successfully!');
      fetchAdminData();
    } catch (error) {
      alert('Failed to approve products');
    }
  };

  if (user?.userprofile?.role !== 'admin' && !user?.is_staff) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <h1 className="text-2xl font-bold text-red-600">Access Denied</h1>
        <p className="text-gray-600">This page is only accessible to administrators.</p>
      </div>
    );
  }

  if (loading) {
    return <Loader text="Loading admin dashboard..." />;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
        <p className="text-gray-600">Manage your e-commerce platform</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Total Products</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.products?.total || 0}</p>
          <p className="text-sm text-gray-500 mt-1">
            {stats.products?.approved || 0} approved, {stats.products?.pending || 0} pending
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Total Users</h3>
          <p className="text-3xl font-bold text-green-600">
            {(stats.users?.customers || 0) + (stats.users?.retailers || 0)}
          </p>
          <p className="text-sm text-gray-500 mt-1">
            {stats.users?.customers || 0} customers, {stats.users?.retailers || 0} retailers
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Total Orders</h3>
          <p className="text-3xl font-bold text-purple-600">{stats.orders?.total || 0}</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Pending Approvals</h3>
          <p className="text-3xl font-bold text-yellow-600">{pendingProducts.length}</p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white rounded-lg shadow-md mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'pending-products', label: `Pending Products (${pendingProducts.length})` },
              { id: 'all-products', label: 'All Products' },
              { id: 'users', label: 'Users' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'overview' && (
            <div>
              <h2 className="text-xl font-semibold mb-6">Platform Overview</h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Recent Activity */}
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="text-lg font-medium mb-4">Recent Activity</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Products awaiting approval</span>
                      <span className="font-medium text-yellow-600">{stats.products?.pending || 0}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Active retailers</span>
                      <span className="font-medium text-green-600">{stats.users?.retailers || 0}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Total customers</span>
                      <span className="font-medium text-blue-600">{stats.users?.customers || 0}</span>
                    </div>
                  </div>
                </div>

                {/* Top Products */}
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="text-lg font-medium mb-4">Top Selling Products</h3>
                  <div className="space-y-3">
                    {stats.top_products?.slice(0, 5).map((product, index) => (
                      <div key={product.id} className="flex items-center justify-between">
                        <div className="flex items-center">
                          <span className="text-sm font-medium text-gray-500 mr-3">#{index + 1}</span>
                          <span className="text-sm text-gray-900">{product.name}</span>
                        </div>
                        <span className="text-sm font-medium text-green-600">${product.price}</span>
                      </div>
                    )) || (
                      <p className="text-sm text-gray-500">No sales data available</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'pending-products' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold">Pending Product Approvals</h2>
                {pendingProducts.length > 0 && (
                  <Button
                    onClick={() => bulkApprove(pendingProducts.map(p => p.id))}
                    variant="primary"
                  >
                    Approve All
                  </Button>
                )}
              </div>

              {pendingProducts.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-500">No products pending approval</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {pendingProducts.map((product) => (
                    <div key={product.id} className="bg-white border border-gray-200 rounded-lg p-6">
                      <img
                        src={product.image || 'https://via.placeholder.com/200x150'}
                        alt={product.name}
                        className="w-full h-32 object-cover rounded-lg mb-4"
                      />
                      
                      <h3 className="font-semibold text-gray-900 mb-2">{product.name}</h3>
                      <p className="text-sm text-gray-600 mb-2">{product.description}</p>
                      <p className="text-lg font-bold text-blue-600 mb-2">${product.price}</p>
                      <p className="text-sm text-gray-500 mb-4">
                        Stock: {product.stock_quantity} | Category: {product.category_name}
                      </p>
                      <p className="text-sm text-gray-500 mb-4">
                        Retailer: {product.retailer_name || 'Unknown'}
                      </p>
                      
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          onClick={() => approveProduct(product.id)}
                          className="flex-1"
                        >
                          Approve
                        </Button>
                        <Button
                          size="sm"
                          variant="danger"
                          onClick={() => {
                            const reason = prompt('Rejection reason (optional):');
                            rejectProduct(product.id, reason);
                          }}
                          className="flex-1"
                        >
                          Reject
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'all-products' && (
            <AllProductsTab />
          )}

          {activeTab === 'users' && (
            <UsersTab />
          )}
        </div>
      </div>
    </div>
  );
};

// All Products Tab Component
const AllProductsTab = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAllProducts();
  }, []);

  const fetchAllProducts = async () => {
    try {
      const response = await api.get('/products/admin/products/');
      setProducts(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loader text="Loading products..." />;
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-6">All Products</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Product
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Retailer
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Price
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Stock
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {products.map((product) => (
              <tr key={product.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <img
                      className="h-10 w-10 rounded object-cover"
                      src={product.image || 'https://via.placeholder.com/40x40'}
                      alt={product.name}
                    />
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">{product.name}</div>
                      <div className="text-sm text-gray-500">{product.category_name}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {product.retailer_name || 'RetailHive'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${product.price}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {product.stock_quantity}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    product.is_approved
                      ? 'bg-green-100 text-green-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {product.is_approved ? 'Approved' : 'Pending'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <Button size="sm" variant="outline">
                    Edit
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Users Tab Component
const UsersTab = () => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-6">User Management</h2>
      <p className="text-gray-600">User management features coming soon...</p>
    </div>
  );
};

export default AdminDashboard;