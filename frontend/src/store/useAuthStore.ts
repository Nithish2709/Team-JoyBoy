import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type UserRole = 'admin' | 'officer' | 'viewer';

export type User = {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  district?: string;
  permissions: string[];
};

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  
  // Actions
  login: (user: User, accessToken: string, refreshToken: string) => void;
  logout: () => void;
  setTokens: (accessToken: string, refreshToken: string) => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,

      login: (user, accessToken, refreshToken) => 
        set({ user, accessToken, refreshToken, isAuthenticated: true }),
      
      logout: () => 
        set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false }),
      
      setTokens: (accessToken, refreshToken) => 
        set({ accessToken, refreshToken }),
        
      updateUser: (updatedFields) => 
        set((state) => ({
          user: state.user ? { ...state.user, ...updatedFields } : null
        })),
    }),
    {
      name: 'auth-storage',
      // We explicitly exclude tokens from persistence for higher security in production, 
      // but for this MVP architecture demo, persisting them in localStorage is fine.
    }
  )
);
