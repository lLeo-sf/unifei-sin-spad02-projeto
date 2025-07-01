import axiosClient from './axiosClient';

export const exportCsv = async (payload) => {
  try {
    const response = await axiosClient.post(
      '/export',
      payload,
      { responseType: 'blob' } 
    );
    return response.data;
  } catch (error) {
    console.error('Erro em searchService:', error);
    throw error;
  }
}