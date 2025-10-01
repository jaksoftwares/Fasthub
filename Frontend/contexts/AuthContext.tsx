'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthAPI } from '@/lib/api/auth';

interface User {
  id: string;
  email: string;
  name: string;
  role: 'customer' | 'admin';
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
}

const AuthContext = createContext<{
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  register: (email: string, password: string, name: string, phone?: string) => Promise<boolean>;
  logout: () => void;
} | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
  });

  useEffect(() => {
    // Check for saved user session
    const savedUser = localStorage.getItem('fasthub-user');
    if (savedUser) {
      setState({ user: JSON.parse(savedUser), isLoading: false });
    } else {
      setState({ user: null, isLoading: false });
    }
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const data = await AuthAPI.login({ username: email, password });
      localStorage.setItem('fasthub-token', data.access_token);
      let user: User;
      const adminEmails = [
        'admin1@fasthub.com',
        'admin2@fasthub.com'
      ];
      try {
        const profile = await AuthAPI.getProfile(data.access_token);
        user = {
          id: profile.id || '',
          email: profile.email || email,
          name: profile.name || email.split('@')[0],
          role: adminEmails.includes(profile.email || email) ? 'admin' : 'customer',
        };
      } catch (profileErr) {
        // fallback if /auth/me is missing or fails
        user = {
          id: '',
          email,
          name: email.split('@')[0],
          role: adminEmails.includes(email) ? 'admin' : 'customer',
        };
      }
      setState({ user, isLoading: false });
      localStorage.setItem('fasthub-user', JSON.stringify(user));
      return true;
    } catch (error) {
      return false;
    }
  };

  const register = async (email: string, password: string, name: string, phone?: string): Promise<boolean> => {
    try {
      await AuthAPI.register({ name, email, phone: phone || '', password });
      // Optionally auto-login after registration
      return await login(email, password);
    } catch (error) {
      return false;
    }
  };

  const logout = async () => {
    const token = localStorage.getItem('fasthub-token');
    if (token) {
      try { await AuthAPI.logout(token); } catch {}
    }
    setState({ user: null, isLoading: false });
    localStorage.removeItem('fasthub-user');
    localStorage.removeItem('fasthub-token');
  };

  return (
    <AuthContext.Provider value={{ ...state, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};