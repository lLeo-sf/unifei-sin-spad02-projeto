import axios, { AxiosInstance } from 'axios';

const axiosClient: AxiosInstance = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 5000
});

export default axiosClient;
