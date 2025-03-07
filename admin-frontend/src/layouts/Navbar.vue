<script setup lang="ts">
import { ref, defineProps } from "vue";
import { useAuthStore } from "../store/auth.ts";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();
const dropdownOpen = ref(false);

defineProps<{ isSidebarCollapsed: boolean }>();

const logout = () => {
  authStore.logout();
  router.push("/");
};
</script>

<template>
  <nav
      class="bg-green-700 p-4 text-white shadow-md fixed top-0 right-0 transition-all duration-300 z-10"
      :class="{ 'left-64': !isSidebarCollapsed, 'left-20': isSidebarCollapsed }"
  >
    <div class="flex justify-between items-center max-w-7xl mx-auto">
      <!-- Title -->
      <h1 class="text-xl font-bold">Dashboard</h1>

      <!-- User Profile -->
      <div class="relative">
        <button
            @click="dropdownOpen = !dropdownOpen"
            class="flex items-center space-x-3 bg-green-800 px-3 py-2 rounded-lg hover:bg-green-900 transition"
        >
          <span class="hidden sm:inline text-white font-medium">Admin</span>
          <div
              class="w-9 h-9 bg-orange-500 rounded-full flex items-center justify-center text-lg font-semibold text-white"
          >
            A
          </div>
        </button>

        <!-- Dropdown Menu -->
        <transition name="fade">
          <div
              v-if="dropdownOpen"
              class="absolute right-0 mt-2 w-52 bg-white text-gray-900 rounded-lg shadow-lg overflow-hidden border border-gray-200"
          >
            <button
                @click="logout"
                class="block w-full text-left px-4 py-3 text-red-600 font-medium hover:bg-gray-100 transition"
            >
              Logout
            </button>
          </div>
        </transition>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>
