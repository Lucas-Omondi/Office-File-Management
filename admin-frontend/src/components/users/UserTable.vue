<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useTimeAgo } from "@vueuse/core";
import { ArrowUpDown, CheckCircle, XCircle, Loader2 } from "lucide-vue-next";
import api from "../../utils/api.ts";

const users = ref<any[]>([]);
const loading = ref(true);
const sortKey = ref<"first_name" | "is_active" | null>(null);
const sortOrder = ref<"asc" | "desc">("asc");

const fetchUsers = async () => {
  try {
    loading.value = true;
    const response = await api.get("users/");
    users.value = response.data;
  } catch (err) {
    console.error("❌ Error fetching users:", err);
  } finally {
    loading.value = false;
  }
};

const toggleActiveStatus = async (userId: number) => {
  try {
    const userIndex = users.value.findIndex((u) => u.id === userId);
    if (userIndex === -1) return; // Ensure user exists

    const response = await api.patch(`users/${userId}/toggle_active/`);

    console.log("✅ User status updated:", response.data); // Debugging

    // Ensure reactivity updates the value
    users.value[userIndex] = { ...users.value[userIndex], is_active: response.data.is_active };
  } catch (err) {
    console.error("❌ Error toggling user status:", err);
  }
};


const sortedUsers = computed(() => {
  if (!sortKey.value) return users.value;

  return [...users.value].sort((a, b) => {
    let aValue = a[sortKey.value];
    let bValue = b[sortKey.value];

    if (sortKey.value === "is_active") {
      aValue = aValue ? 1 : 0;
      bValue = bValue ? 1 : 0;
    }

    return sortOrder.value === "asc"
        ? aValue > bValue ? 1 : -1
        : aValue < bValue ? 1 : -1;
  });
});

const toggleSort = (key: "first_name" | "is_active") => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  } else {
    sortKey.value = key;
    sortOrder.value = "asc";
  }
};

const getLastSeen = (timestamp: string | null) => {
  if (!timestamp) return "Never";
  return useTimeAgo(new Date(timestamp)).value;
};

onMounted(fetchUsers);
</script>

<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6 text-gray-800">👥 Users</h1>

    <div v-if="loading" class="flex items-center justify-center text-gray-500">
      <Loader2 class="animate-spin w-6 h-6 mr-2" /> Loading users...
    </div>

    <div v-else class="overflow-x-auto bg-white shadow-md rounded-lg">
      <table class="w-full border-collapse">
        <thead>
        <tr class="bg-gray-800 text-white text-left">
          <th class="p-4">Username</th>
          <th class="p-4 cursor-pointer hover:bg-gray-700 flex items-center" @click="toggleSort('first_name')">
            First Name
            <ArrowUpDown class="ml-2 w-4 h-4" />
          </th>
          <th class="p-4">Last Name</th>
          <th class="p-4">Email</th>
          <th class="p-4">Role</th>
          <th class="p-4">Last Seen</th>
          <th class="p-4 cursor-pointer hover:bg-gray-700 flex items-center" @click="toggleSort('is_active')">
            Active Status
            <ArrowUpDown class="ml-2 w-4 h-4" />
          </th>
          <th class="p-4">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="user in sortedUsers" :key="user.id" class="border-b hover:bg-gray-50 transition">
          <td class="p-4">{{ user.username }}</td>
          <td class="p-4">{{ user.first_name }}</td>
          <td class="p-4">{{ user.last_name }}</td>
          <td class="p-4">{{ user.email }}</td>
          <td class="p-4 capitalize">{{ user.role }}</td>
          <td class="p-4">
              <span class="px-2 py-1 text-sm font-medium rounded"
                    :class="user.last_login ? 'bg-blue-100 text-blue-700' : 'bg-gray-200 text-gray-600'">
                {{ getLastSeen(user.last_login) }}
              </span>
          </td>
          <td class="p-4">
            <span
                class="flex items-center px-2 py-1 text-sm font-semibold rounded-full transition-all"
                :class="user.is_active
                ? 'bg-green-100 text-green-700 border border-green-500 shadow-sm'
                : 'bg-red-100 text-red-700 border border-red-500 shadow-sm'">
                <CheckCircle v-if="user.is_active" class="w-4 h-4 mr-1" />
                <XCircle v-else class="w-4 h-4 mr-1" />
                {{ user.is_active ? "Active" : "Inactive" }}
            </span>
          </td>
          <td class="p-4">
            <button
                @click="toggleActiveStatus(user.id)"
                class="px-3 py-1 text-sm font-semibold rounded transition flex items-center"
                :class="user.is_active ? 'bg-red-500 text-white hover:bg-red-600' : 'bg-green-500 text-white hover:bg-green-600'"
            >
              <XCircle v-if="user.is_active" class="w-4 h-4 mr-1" />
              <CheckCircle v-else class="w-4 h-4 mr-1" />
              {{ user.is_active ? "Deactivate" : "Activate" }}
            </button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
