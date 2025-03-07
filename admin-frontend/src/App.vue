<script setup lang="ts">
import { ref, computed } from "vue";
import { useAuthStore } from "./store/auth.ts";
import { useRoute, RouterView } from "vue-router";
import Sidebar from "./components/Sidebar.vue";
import Navbar from "./layouts/Navbar.vue"; // Import Navbar

const authStore = useAuthStore();
const route = useRoute();

const isSidebarCollapsed = ref(false);

// Compute authentication status
const isAuthenticated = computed(() => !!authStore.token);

// Compute if the current page is login
const isLoginPage = computed(() => route.path === "/");

// Receive event from Sidebar.vue
const handleSidebarToggle = (collapsed: boolean) => {
  isSidebarCollapsed.value = collapsed;
};
</script>

<template>


  <div class="flex">
    <!-- Show Sidebar only if authenticated and NOT on login page -->
    <Sidebar
        v-if="isAuthenticated && !isLoginPage"
        @toggle-sidebar="handleSidebarToggle"
    />

    <!-- Main Content Area -->
    <div
        class="transition-all duration-300 min-h-screen"
        :class="{
        'ml-64 w-[calc(100%-16rem)]': isAuthenticated && !isSidebarCollapsed && !isLoginPage,
        'ml-20 w-[calc(100%-5rem)]': isAuthenticated && isSidebarCollapsed && !isLoginPage,
        'w-full': isLoginPage || !isAuthenticated, // Full width if login page or not authenticated
      }"
    >
      <!-- Show Navbar only if authenticated and NOT on login page -->
      <Navbar v-if="isAuthenticated && !isLoginPage" />

      <main class="p-4">
        <RouterView :sidebarExpanded="!isSidebarCollapsed" />

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
