import { defineStore } from "pinia";
import api from "../utils/api";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        accessToken: localStorage.getItem("accessToken") || null,
        refreshToken: localStorage.getItem("refreshToken") || null,
        user: JSON.parse(localStorage.getItem("user") || "null"),
    }),

    getters: {
        isAuthenticated(): boolean {
            return !!this.accessToken && !!this.user;
        },
    },

    actions: {
        async login(username: string, password: string) {
            try {
                const response = await api.post("token/", { username, password });

                this.setAccessToken(response.data.access);
                this.setRefreshToken(response.data.refresh);

                console.log("✅ Login successful. Fetching user data...");
                const userResponse = await this.fetchUserData();

                if (userResponse) {
                    return true;
                } else {
                    console.warn("⚠️ User fetch failed after login. Logging out...");
                    this.logout();
                    return false;
                }
            } catch (error) {
                console.error("❌ Login error:", error.response?.data || error.message);
                return false;
            }
        },

        async fetchUserData(retry = true) {
            try {
                console.log("🔄 Fetching user data...");
                const userResponse = await api.get("/me/");
                this.setUser(userResponse.data);
                console.log("✅ User data fetched successfully:", userResponse.data);
                return true;
            } catch (error) {
                if (error.response?.status === 401 && retry) {
                    console.warn("🔄 Token expired. Refreshing token...");
                    const refreshed = await this.refreshAccessToken();
                    if (refreshed) {
                        return this.fetchUserData(false); // Retry once
                    }
                }
                console.error("❌ User fetch error:", error.response?.data || error.message);
                return false;
            }
        },

        async refreshAccessToken() {
            if (!this.refreshToken) {
                console.warn("⚠️ No refresh token found. Logging out...");
                this.logout();
                return false;
            }

            try {
                console.log("🔄 Refreshing access token...");
                const response = await api.post("token/refresh/", { refresh: this.refreshToken });

                if (response.data.access) {
                    console.log("✅ Token refreshed successfully");
                    this.setAccessToken(response.data.access);
                    return true;
                }
            } catch (error) {
                console.error("❌ Token refresh failed:", error.response?.data || error.message);
                this.logout(); // Ensure user is logged out on failure
                return false;
            }
        },

        setAccessToken(token: string) {
            this.accessToken = token;
            localStorage.setItem("accessToken", token);
            api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
            console.log("🔐 Access token set:", token);
        },

        setRefreshToken(token: string) {
            this.refreshToken = token;
            localStorage.setItem("refreshToken", token);
            console.log("🔄 Refresh token stored.");
        },

        setUser(userData: any) {
            this.user = userData;
            localStorage.setItem("user", JSON.stringify(userData));
            console.log("👤 User data stored:", userData);
        },

        logout() {
            console.warn("🚪 Logging out user...");
            this.accessToken = null;
            this.refreshToken = null;
            this.user = null;

            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
            localStorage.removeItem("user");

            delete api.defaults.headers.common["Authorization"];
        },
    },
});
