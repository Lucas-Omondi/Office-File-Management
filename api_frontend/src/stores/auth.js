import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("access_token") || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },
  actions: {
    setToken(token) {
      this.accessToken = token;
      localStorage.setItem("access_token", token);
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    },
    logout() {
      this.accessToken = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      axios.defaults.headers.common["Authorization"] = null;
    },
  },
});
