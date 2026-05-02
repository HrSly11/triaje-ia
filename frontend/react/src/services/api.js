import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
});

api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const login = async (username, password) => {
  const response = await api.post('/auth/login', { nombre_usuario: username, contrasena: password });
  return response.data;
};

export const getPacientes = async (search = '', page = 1) => {
  const response = await api.get('/pacientes', { params: { busqueda: search, page, per_page: 20 } });
  return response.data;
};

export const getPaciente = async (id) => {
  const response = await api.get(`/pacientes/${id}`);
  return response.data;
};

export const createPaciente = async (data) => {
  const response = await api.post('/pacientes', data);
  return response.data;
};

export const getTriajes = async (params = {}) => {
  const response = await api.get('/triajes', { params });
  return response.data;
};

export const getTriaje = async (id) => {
  const response = await api.get(`/triajes/${id}`);
  return response.data;
};

export const createTriaje = async (data) => {
  const response = await api.post('/triajes', data);
  return response.data;
};

export const completarTriaje = async (id, data) => {
  const response = await api.put(`/triajes/${id}/completar`, data);
  return response.data;
};

export const getDashboardOperacional = async (fecha) => {
  const response = await api.get('/dashboard/operacional', { params: { fecha } });
  return response.data;
};

export const getDashboardGestion = async (mes) => {
  const response = await api.get('/dashboard/gestion', { params: { mes } });
  return response.data;
};

export const getAntecedentesHCE = async (numeroDocumento) => {
  const response = await api.get(`/hce/${numeroDocumento}/antecedentes`);
  return response.data;
};

export default api;
