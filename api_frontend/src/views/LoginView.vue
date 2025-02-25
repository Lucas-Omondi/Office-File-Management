<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Login</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import axios from "axios";

const username = ref("");
const password = ref("");
const error = ref("");
const authStore = useAuthStore();
const router = useRouter();

const login = async () => {
  error.value = "";
  try {
    console.log("Sending request:", { username: username.value, password: password.value });

    const response = await axios.post("http://127.0.0.1:8000/api/token/", {
      username: username.value,
      password: password.value,
    });

    console.log("Login successful:", response.data);

    // Store token in Pinia and LocalStorage
    authStore.setToken(response.data.access);
    localStorage.setItem("access_token", response.data.access);
    localStorage.setItem("refresh_token", response.data.refresh);

    // Redirect to Dashboard
    await router.push("/dashboard");
  } catch (err) {
    console.error("Login error:", err.response?.data || err.message);
    error.value = "Invalid username or password. Try again.";
  }
};
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: 50px auto;
  text-align: center;
}
input {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}
button {
  background: #42b983;
  color: white;
  padding: 8px 15px;
  border: none;
  cursor: pointer;
}
.error {
  color: red;
}
</style>
