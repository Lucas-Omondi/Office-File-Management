import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
    timeout: 10000,
});

// Add a request interceptor
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("accessToken");

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
            console.log("✅ Token Attached:", token);
        } else {
            console.warn("⚠️ No token found in localStorage");
        }

        console.log("📡 Axios Request Headers:", config.headers); // Log full headers
        console.log("🌐 Request URL:", config.url);
        console.log("📨 Request Method:", config.method);

        return config;
    },
    (error) => {
        console.error("❌ Request Interceptor Error:", error);
        return Promise.reject(error);
    }
);

// Add a response interceptor
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error("❌ Axios Response Error:", error.response);
        console.error("⚠️ Response Status:", error.response?.status);
        console.error("📨 Response Headers:", error.response?.headers);
        return Promise.reject(error);
    }
);

export default api;
