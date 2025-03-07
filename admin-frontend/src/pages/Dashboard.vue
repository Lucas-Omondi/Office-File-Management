<script setup lang="ts">
import { ref } from "vue";
import Sidebar from "../components/Sidebar.vue";
import Navbar from "../layouts/Navbar.vue";

const isSidebarCollapsed = ref(false);
const handleSidebarToggle = (collapsed: boolean) => {
  isSidebarCollapsed.value = collapsed;
};

const stats = [
  { label: "Projects", count: 120, color: "bg-green-500" },
  { label: "Users", count: 50, color: "bg-blue-500" },
  { label: "Constituencies", count: 80, color: "bg-orange-500" },
  { label: "Files", count: 300, color: "bg-purple-500" },
];
</script>

<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <Sidebar class="fixed left-0 top-0 h-full" @toggle-sidebar="handleSidebarToggle" />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col transition-all duration-300"
         :class="{ 'ml-64': !isSidebarCollapsed, 'ml-20': isSidebarCollapsed }">
      <!-- Navbar -->
      <Navbar :isSidebarCollapsed="isSidebarCollapsed" />

      <!-- Page Content -->
      <main class="mt-16 p-6">
        <h2 class="text-3xl font-semibold text-gray-800">Dashboard</h2>
        <p class="text-gray-600 mb-6">Welcome! Here’s an overview of the system.</p>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="stat in stats" :key="stat.label" class="p-6 rounded-lg shadow-md text-white" :class="stat.color">
            <h3 class="text-2xl font-bold">{{ stat.count }}</h3>
            <p class="text-lg">{{ stat.label }}</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
