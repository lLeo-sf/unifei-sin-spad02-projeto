import axios from 'axios';

const axiosClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/',
  timeout: 5000,
});

export default axiosClient;