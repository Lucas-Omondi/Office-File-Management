<script setup lang="ts">
import { ref, computed } from "vue";
import { useAuthStore } from "./store/auth.ts";
import { RouterView } from "vue-router";
import Sidebar from "./components/Sidebar.vue";

const authStore = useAuthStore();
const isSidebarCollapsed = ref(false);

// Compute authentication status
const isAuthenticated = computed(() => !!authStore.token);

// Receive event from Sidebar.vue
const handleSidebarToggle = (collapsed: boolean) => {
  isSidebarCollapsed.value = collapsed;
};
</script>

<template>
  <div class="flex">
    <!-- Show Sidebar only if authenticated -->
    <Sidebar v-if="isAuthenticated" @toggle-sidebar="handleSidebarToggle" />

    <!-- Main Content Area -->
    <div
        class="transition-all duration-300 p-6"
        :class="{
        'ml-64 w-[calc(100%-16rem)]': isAuthenticated && !isSidebarCollapsed,
        'ml-20 w-[calc(100%-5rem)]': isAuthenticated && isSidebarCollapsed,
        'w-full': !isAuthenticated, // Full width if not authenticated
      }"
    >
      <header
          v-if="isAuthenticated"
          class="flex justify-between p-4 bg-green-700 text-white"
      >
        <h1 class="text-lg font-bold">Admin Dashboard</h1>
        <button
            @click="authStore.logout"
            class="px-4 py-2 bg-red-500 rounded hover:bg-red-600"
        >
          Logout
        </button>
      </header>

      <main class="transition-all duration-300">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Smooth transition for main content */
main {
  transition: margin-left 0.3s ease-in-out, width 0.3s ease-in-out;
}
</style>
