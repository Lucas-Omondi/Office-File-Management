import { defineStore } from "pinia";
import api from "../utils/api";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        accessToken: localStorage.getItem("accessToken") || null,
        refreshToken: localStorage.getItem("refreshToken") || null,
    }),
    actions: {
        async login(username: string, password: string) {
            try {
                const response = await api.post("token/", { username, password });

                this.setAccessToken(response.data.access);
                this.setRefreshToken(response.data.refresh);

                return true;
            } catch (error) {
                console.error("Login error:", error.response?.data || error.message);
                return false;
            }
        },
        async refreshAccessToken() {
            if (!this.refreshToken) return false; // No refresh token available

            try {
                const response = await api.post("token/refresh/", { refresh: this.refreshToken });
                this.setAccessToken(response.data.access);
                return true;
            } catch (error) {
                console.error("Token refresh error:", error.response?.data || error.message);
                this.logout();
                return false;
            }
        },
        setAccessToken(token: string) {
            this.accessToken = token;
            localStorage.setItem("accessToken", token);

            // 🔹 Update Axios headers globally
            api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        },
        setRefreshToken(token: string) {
            this.refreshToken = token;
            localStorage.setItem("refreshToken", token);
        },
        logout() {
            this.accessToken = null;
            this.refreshToken = null;
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");

            // 🔹 Remove Authorization header on logout
            delete api.defaults.headers.common["Authorization"];
        },
    },
});
