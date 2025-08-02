import api from './axios';

export const ordersAPI = {
  getOrders: async () => {
    try {
      const response = await api.get('/orders/orders/');
      return response.data || [];
    } catch (error) {
      console.error('Error fetching orders:', error);
      return [];
    }
  },

  createOrder: async (orderData) => {
    try {
      const response = await api.post('/orders/orders/create_order/', orderData);
      return response.data;
    } catch (error) {
      console.error('Error creating order:', error);
      throw error;
    }
  },

  getCart: async () => {
    try {
      const response = await api.get('/orders/cart/');
      return response.data || { items: [], total_items: 0, total_price: 0 };
    } catch (error) {
      console.error('Error fetching cart:', error);
      return { items: [], total_items: 0, total_price: 0 };
    }
  },

  addToCart: async (itemData) => {
    try {
      const response = await api.post('/orders/cart/add/', itemData);
      return response.data;
    } catch (error) {
      console.error('Error adding to cart:', error);
      throw error;
    }
  },

  removeFromCart: async (itemId) => {
    try {
      const response = await api.delete(`/orders/cart/remove/${itemId}/`);
      return response.data;
    } catch (error) {
      console.error('Error removing from cart:', error);
      throw error;
    }
  }
};