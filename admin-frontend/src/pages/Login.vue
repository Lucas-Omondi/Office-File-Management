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
  <div class="w-full h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-blue-900 to-indigo-800">
    <v-motion
        :initial="{ opacity: 0, y: -20 }"
        :animate="{ opacity: 1, y: 0 }"
        :transition="{ duration: 0.6, easing: 'easeOut' }"
        class="w-full max-w-md bg-white/10 backdrop-blur-md shadow-2xl rounded-2xl border border-white/20 p-8 relative"
    >
      <div class="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-500/30 to-indigo-500/30 blur-xl opacity-50"></div>

      <h2 class="text-4xl font-bold text-white text-center mb-8 relative z-10">Welcome Back</h2>

      <form @submit.prevent="login" class="space-y-6 relative z-10">
        <!-- Username Field -->
        <div class="relative">
          <input
              v-model="username"
              type="text"
              id="username"
              placeholder=" "
              class="peer w-full p-4 bg-transparent border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-white backdrop-blur-lg"
              required
          />
          <label
              for="username"
              class="absolute left-4 text-gray-300 text-sm transition-all duration-200 ease-in-out
                   peer-placeholder-shown:top-4 peer-placeholder-shown:text-gray-400 peer-placeholder-shown:text-base
                   peer-focus:top-1 peer-focus:text-xs peer-focus:text-blue-400"
              :class="{ 'top-1 text-xs text-blue-400': username }"
          >
          Username
          </label>
        </div>

        <!-- Password Field -->
        <div class="relative">
          <input
              v-model="password"
              type="password"
              id="password"
              placeholder=" "
              class="peer w-full p-4 bg-transparent border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-white backdrop-blur-lg"
              required
          />
          <label
              for="password"
              class="absolute left-4 text-gray-300 text-sm transition-all duration-200 ease-in-out
                   peer-placeholder-shown:top-4 peer-placeholder-shown:text-gray-400 peer-placeholder-shown:text-base
                   peer-focus:top-1 peer-focus:text-xs peer-focus:text-blue-400"
              :class="{ 'top-1 text-xs text-blue-400': password }"
          >
          Password
          </label>
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="text-red-400 text-sm text-center animate-fade-in">
          {{ errorMessage }}
        </p>

        <!-- Login Button -->
        <button
            v-motion
            :while-hover="{ scale: 1.05 }"
            :while-tap="{ scale: 0.95 }"
            type="submit"
            class="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white font-semibold rounded-lg transition-all shadow-lg shadow-blue-500/50"
        >
          Login
        </button>
      </form>

      <p class="mt-6 text-sm text-gray-300 text-center">
        Don't have an account? <a href="#" class="text-blue-400 hover:underline">Sign up</a>
      </p>
    </v-motion>
  </div>
</template>


<style scoped>
/* Smooth fade-in animation */
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
