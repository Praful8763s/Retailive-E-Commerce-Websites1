import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext.jsx';
import { useCart } from '../contexts/CartContext.jsx';
import Button from './Button.jsx';

const NavBar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const { cartItemsCount } = useCart();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <Link to="/" className="text-2xl font-bold text-primary-600">
            RetailHive
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-6">
            <Link to="/" className="text-gray-700 hover:text-primary-600 transition-colors">
              Home
            </Link>
            <Link to="/products" className="text-gray-700 hover:text-primary-600 transition-colors">
              Products
            </Link>
            
            {isAuthenticated ? (
              <>
                {/* Role-based navigation */}
                {user?.userprofile?.role === 'admin' || user?.is_staff ? (
                  <Link to="/admin-dashboard" className="text-gray-700 hover:text-primary-600 transition-colors">
                    Admin Dashboard
                  </Link>
                ) : user?.userprofile?.role === 'retailer' ? (
                  <Link to="/retailer-dashboard" className="text-gray-700 hover:text-primary-600 transition-colors">
                    Retailer Dashboard
                  </Link>
                ) : (
                  <>
                    <Link to="/dashboard" className="text-gray-700 hover:text-primary-600 transition-colors">
                      Dashboard
                    </Link>
                    <Link to="/cart" className="relative text-gray-700 hover:text-primary-600 transition-colors">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.5 6M7 13l-1.5 6m0 0h9m-9 0V19a2 2 0 002 2h7a2 2 0 002-2v-.5" />
                      </svg>
                      {cartItemsCount > 0 && (
                        <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                          {cartItemsCount}
                        </span>
                      )}
                    </Link>
                  </>
                )}
                
                <Link to="/profile" className="text-gray-700 hover:text-primary-600 transition-colors">
                  Profile
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-gray-700 hover:text-primary-600 transition-colors"
                >
                  Logout
                </button>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-500">
                    Welcome, {user?.username}
                  </span>
                  {user?.userprofile?.role && (
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      user.userprofile.role === 'admin' ? 'bg-red-100 text-red-800' :
                      user.userprofile.role === 'retailer' ? 'bg-blue-100 text-blue-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {user.userprofile.role.charAt(0).toUpperCase() + user.userprofile.role.slice(1)}
                    </span>
                  )}
                </div>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="outline" size="sm">Login</Button>
                </Link>
                <Link to="/register">
                  <Button size="sm">Register</Button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden text-gray-700"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t">
            <div className="flex flex-col space-y-2">
              <Link to="/" className="text-gray-700 hover:text-primary-600 py-2 transition-colors">
                Home
              </Link>
              <Link to="/products" className="text-gray-700 hover:text-primary-600 py-2 transition-colors">
                Products
              </Link>
              
              {isAuthenticated ? (
                <>
                  <Link to="/dashboard" className="text-gray-700 hover:text-primary-600 py-2 transition-colors">
                    Dashboard
                  </Link>
                  <Link to="/cart" className="text-gray-700 hover:text-primary-600 py-2 transition-colors">
                    Cart ({cartItemsCount})
                  </Link>
                  <Link to="/profile" className="text-gray-700 hover:text-primary-600 py-2 transition-colors">
                    Profile
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="text-left text-gray-700 hover:text-primary-600 py-2 transition-colors"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-gray-700 hover:text-primary-600 py-2 transition-colors">
                    Login
                  </Link>
                  <Link to="/register" className="text-gray-700 hover:text-primary-600 py-2 transition-colors">
                    Register
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default NavBar;