import apiClient from './api';

export const analyzeIris = async (query) => {
  const response = await apiClient.post('/api/v1/analyze', {
    query,
  });
  return response.data;
};

export const checkHealth = async () => {
  const response = await apiClient.get('/health/ready');
  return response.data;
};
