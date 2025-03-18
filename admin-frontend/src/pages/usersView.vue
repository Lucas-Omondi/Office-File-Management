<template>
  <div class="flex">
    <!-- Sidebar -->
    <Sidebar
        v-if="isAuthenticated"
        class="fixed left-0 top-0 h-full"
        @toggle-sidebar="handleSidebarToggle"
    />

    <!-- Main Content Area -->
    <div
        class="transition-all duration-300 min-h-screen p-6 pt-16"
        :class="{
        'ml-64 w-[calc(100%-16rem)]': isAuthenticated && !isSidebarCollapsed,
        'ml-20 w-[calc(100%-5rem)]': isAuthenticated && isSidebarCollapsed,
        'w-full': !isAuthenticated,
        }">
      <!-- Navbar -->
      <Navbar
          v-if="isAuthenticated"
          :isSidebarCollapsed="isSidebarCollapsed"
          class="fixed top-0 left-0 w-full z-10"
      />

      <!-- Page Content -->
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold">User Management</h1>
        <button @click="isAddUserOpen = true" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          + Add User
        </button>
      </div>
    <!-- View Mode Toggle -->
    <div class="mb-4 flex items-center gap-2">
      <span class="text-gray-600">View Mode:</span>
      <button
          @click="viewMode = 'table'"
          :class="{ 'bg-gray-300': viewMode === 'table' }"
          class="px-3 py-1 border rounded-md"
      >
        Table
      </button>
      <button
          @click="viewMode = 'grid'"
          :class="{ 'bg-gray-300': viewMode === 'grid' }"
          class="px-3 py-1 border rounded-md"
      >
        Grid
      </button>
    </div>


      <UserTable v-if="viewMode === 'table'" :users="users" />
      <UserGrid v-else :users="users" />
      <AddUserModal
          v-if="isAddUserOpen"
          :isOpen="isAddUserOpen"
          @close="isAddUserOpen = false"
          @added="addUserToList"
      />


    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import UserTable from "../components/users/UserTable.vue";
import UserGrid from "../components/users/UserGrid.vue";
import api from "../utils/api.js";
import { useAuthStore } from "../store/auth.js";
import Navbar from "../layouts/Navbar.vue";
import Sidebar from "../components/Sidebar.vue";
import AddUserModal from "../components/users/modals/AddUserModal.vue";

const users = ref([]);
const isAddUserOpen = ref(false);
const viewMode = ref("table");
const authStore = useAuthStore();
const isAuthenticated = computed(() => !!authStore.accessToken);

// Sidebar state
const isSidebarCollapsed = ref(true);
const handleSidebarToggle = (collapsed) => {
  isSidebarCollapsed.value = collapsed;
};

// Fetch users
const fetchUsers = async () => {
  try {
    const response = await api.get("users/");
    users.value = response.data;
  } catch (error) {
    console.error("Failed to fetch users:", error);
  }
};
// Add New User to List
const addUserToList = (newUser: any) => {
  users.value.unshift(newUser);
  isAddUserOpen.value = false;
};

onMounted(fetchUsers);
onMounted(() => {
  console.log("🔍 Checking auth store on mount...");
  console.log("✅ Access Token:", authStore.accessToken);
  console.log("✅ Is Authenticated:", !!authStore.accessToken);
});
</script>

<style scoped>
button {
  transition: background-color 0.2s;
}
</style>
