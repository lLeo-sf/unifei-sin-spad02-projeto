import axiosClient from './axiosClient';

export const getMetadata = async () => {
  try {
    const response = await axiosClient.get('/metadata');
    return response.data;
  } catch (error) {
    console.error('Erro em metadataService:', error);
    throw error;
  }
};