import axiosClient from './axiosClient';

export const search = async (payload) => {
  try {
    const response = await axiosClient.post('/search', payload);
    return response.data;
  } catch (error) {
    console.error('Erro em searchService:', error);
    throw error;
  }
};