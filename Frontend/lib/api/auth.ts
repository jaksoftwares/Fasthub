
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://0.0.0.0:8000';

export const AuthAPI = {
  register: async (data: { name: string; email: string; phone: string; password: string }) => {
    const res = await axios.post(`${API_URL}/auth/register`, data);
    return res.data;
  },
  login: async (data: { username: string; password: string }) => {
    const params = new URLSearchParams();
    params.append('username', data.username);
    params.append('password', data.password);
    return (await axios.post(`${API_URL}/auth/login`, params, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })).data;
  },
  logout: async (token: string) => {
    return (await axios.post(`${API_URL}/auth/logout`, {}, { headers: { Authorization: `Bearer ${token}` } })).data;
  },
  refresh: async (token: string) => {
    return (await axios.post(`${API_URL}/auth/refresh`, token, { headers: { 'Content-Type': 'application/json' } })).data;
  },
  getCustomers: async (token: string) => {
    return (await axios.get(`${API_URL}/auth/customers`, { headers: { Authorization: `Bearer ${token}` } })).data;
  },
  getProfile: async (token: string) => {
    return (await axios.get(`${API_URL}/auth/me`, { headers: { Authorization: `Bearer ${token}` } })).data;
  },
};
