// TypeScript module declaration for the API utility
// This fixes 'Cannot find module ./api' errors

declare module "lib/api" {
  export const api: {
    get: <T = any>(endpoint: string) => Promise<T>;
    post: <T = any>(endpoint: string, body?: any) => Promise<T>;
    put: <T = any>(endpoint: string, body?: any) => Promise<T>;
    delete: <T = any>(endpoint: string) => Promise<T>;
  };
  export function apiRequest<T = any>(endpoint: string, options?: RequestInit): Promise<T>;
}
