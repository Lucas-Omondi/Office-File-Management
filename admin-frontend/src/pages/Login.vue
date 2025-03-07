<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from "../store/auth";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const authStore = useAuthStore();
const router = useRouter();
const errorMessage = ref("");

const login = async () => {
  const success = await authStore.login(username.value, password.value);
  if (success) {
    console.log("Login successful, redirecting...");
    router.push("/dashboard");
  } else {
    errorMessage.value = "Invalid username or password.";
  }
};
</script>

<template>
  <div class="w-full h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-blue-800 to-indigo-700">
    <div
        v-motion
        :initial="{ opacity: 0, y: -20 }"
        :animate="{ opacity: 1, y: 0 }"
        :transition="{ duration: 0.6, easing: 'easeOut' }"
        class="w-full max-w-md bg-white/20 backdrop-blur-md shadow-2xl rounded-2xl border border-white/30"
    >
      <div class="px-8 py-4"> <!-- ✅ Added padding only inside to avoid extra space -->
        <h2 class="text-3xl font-semibold text-white text-center mb-6">Welcome Back</h2>
        <form @submit.prevent="login" class="space-y-4">
          <div>
            <label class="text-white block text-sm font-medium mb-1">Username</label>
            <input
                v-model="username"
                type="text"
                class="w-full p-3 bg-white/10 border border-white/40 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 text-white placeholder-gray-300"
                placeholder="Enter your username"
                required
            />
          </div>
          <div>
            <label class="text-white block text-sm font-medium mb-1">Password</label>
            <input
                v-model="password"
                type="password"
                class="w-full p-3 bg-white/10 border border-white/40 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 text-white placeholder-gray-300"
                placeholder="Enter your password"
                required
            />
          </div>
          <button
              v-motion
              :while-hover="{ scale: 1.05 }"
              :while-tap="{ scale: 0.95 }"
              type="submit"
              class="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white font-semibold rounded-lg transition-all shadow-lg"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  </div>

</template>
