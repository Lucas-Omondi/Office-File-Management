<script setup lang="ts">
import { ref, defineEmits } from "vue";
import { useRouter, useRoute } from "vue-router";
import { Menu, Home, Folder, FileText, Users, MapPin, Globe, LayoutDashboard } from "lucide-vue-next";

const router = useRouter();
const route = useRoute();
const isCollapsed = ref(true);
const emit = defineEmits(["toggle-sidebar"]);

// Toggle sidebar and notify parent
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
  emit("toggle-sidebar", isCollapsed.value);
};

// Navigation Items
const navItems = [
  { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { name: "Projects", path: "/projects", icon: Folder },
  { name: "Files", path: "/files", icon: FileText },
  { name: "Constituencies", path: "/constituencies", icon: MapPin },
  { name: "Users", path: "/users", icon: Users },
  { name: "Counties", path: "/counties", icon: Globe },
];

const isActive = (path: string) => route.path === path;
const navigateTo = (path: string) => router.push(path);
</script>

<template>
  <aside
      class="fixed left-0 top-16 transition-all duration-300 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 shadow-xl flex flex-col"
      :class="{ 'w-64': !isCollapsed, 'w-20': isCollapsed }"
      style="height: calc(100vh - 4rem);"
  >
    <div class="flex items-center justify-between px-4 py-4">
      <h1 v-if="!isCollapsed" class="text-lg font-semibold text-gray-800 dark:text-gray-200">Admin Panel</h1>
      <button
          @click="toggleSidebar"
          class="p-2 bg-gray-200 dark:bg-gray-700 rounded-full hover:bg-gray-300 dark:hover:bg-gray-600 transition"
      >
        <Menu class="w-5 h-5 text-gray-600 dark:text-gray-300" />
      </button>
    </div>

    <nav class="mt-4 space-y-2">
      <button
          v-for="item in navItems"
          :key="item.path"
          @click="navigateTo(item.path)"
          class="flex items-center space-x-3 p-3 rounded-lg group transition-all duration-300 w-full"
          :class="{
          'bg-gradient-to-r from-green-500 to-green-700 text-white shadow-lg': isActive(item.path),
          'hover:bg-gray-100 dark:hover:bg-gray-800': !isActive(item.path),
        }"
      >
        <component :is="item.icon" class="w-5 h-5 text-gray-600 dark:text-gray-300 group-hover:text-green-600 dark:group-hover:text-green-400" />
        <span v-if="!isCollapsed" class="text-gray-700 dark:text-gray-300 font-medium group-hover:text-green-600 dark:group-hover:text-green-400">
          {{ item.name }}
        </span>
      </button>
    </nav>
  </aside>
</template>
