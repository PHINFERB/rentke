import api from '../api';

export const getProperties = async (params = {}) => {
  try {
    const response = await api.get('/properties/', { params });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getProperty = async (id) => {
  try {
    const response = await api.get(`/properties/${id}/`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const createProperty = async (propertyData) => {
  try {
    const formData = new FormData();
    for (const key in propertyData) {
      formData.append(key, propertyData[key]);
    }
    const response = await api.post('/properties/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};