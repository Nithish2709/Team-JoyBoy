import apiClient from './apiClient';
import { User } from '../store/useAuthStore';

// Mock responses for development without a real backend
const MOCK_DELAY = 1000;

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const authApi = {
  login: async (credentials: { email: string; password: string }) => {
    // In a real app: return apiClient.post('/auth/login', credentials);
    await delay(MOCK_DELAY);
    
    if (credentials.email === 'admin@pds.tn.gov.in' && credentials.password === 'password') {
      return {
        data: {
          access_token: 'mock_access_token_abc123',
          refresh_token: 'mock_refresh_token_xyz789',
          user: {
            id: 'usr_001',
            name: 'System Admin',
            email: 'admin@pds.tn.gov.in',
            role: 'admin',
            permissions: ['read:all', 'write:all', 'delete:all']
          }
        }
      };
    }
    
    throw { response: { status: 401, data: { message: 'Invalid credentials' } } };
  },

  logout: async () => {
    // In a real app: return apiClient.post('/auth/logout');
    await delay(500);
    return { data: { success: true } };
  },

  getMe: async () => {
    return apiClient.get<User>('/users/me');
  }
};
