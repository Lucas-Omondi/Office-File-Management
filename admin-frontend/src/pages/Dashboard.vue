<script setup lang="ts">
import Sidebar from "../components/Sidebar.vue";
import Navbar from "../layouts/Navbar.vue";
</script>

<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <!-- Navbar -->
      <Navbar />

      <!-- Page Content -->
      <main class="flex-1 p-6">
        <h2 class="text-2xl font-semibold text-gray-800">Dashboard</h2>
        <p class="text-gray-600 mt-2">Welcome! Select a category from the sidebar.</p>
      </main>
    </div>
  </div>
</template>

<style scoped>
main {
  transition: all 0.3s ease-in-out;
}
</style>
