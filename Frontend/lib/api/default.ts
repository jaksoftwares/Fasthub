import { api } from "lib/api";

export const DefaultAPI = {
  root: () => api.get("/"),
  health: () => api.get("/health"),
};
