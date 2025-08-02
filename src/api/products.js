import api from './axios';

export const productsAPI = {
  getProducts: async (params = {}) => {
    try {
      const response = await api.get('/products/products/', { params });
      return response.data || [];
    } catch (error) {
      console.error('Error fetching products:', error);
      return [];
    }
  },

  getProduct: async (id) => {
    try {
      const response = await api.get(`/products/products/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching product:', error);
      throw error;
    }
  },

  searchProducts: async (query) => {
    try {
      const response = await api.get('/products/products/search/', {
        params: { q: query }
      });
      return response.data || [];
    } catch (error) {
      console.error('Error searching products:', error);
      return [];
    }
  },

  getCategories: async () => {
    try {
      const response = await api.get('/products/categories/');
      return response.data || [];
    } catch (error) {
      console.error('Error fetching categories:', error);
      return [];
    }
  },

  addReview: async (productId, reviewData) => {
    try {
      const response = await api.post(`/products/products/${productId}/add_review/`, reviewData);
      return response.data;
    } catch (error) {
      console.error('Error adding review:', error);
      throw error;
    }
  }
};