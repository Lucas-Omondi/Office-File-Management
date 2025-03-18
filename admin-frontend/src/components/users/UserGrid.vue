<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6 text-gray-800">👥 Users</h1>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center text-gray-500">
      <Loader2 class="animate-spin w-6 h-6 mr-2" /> Loading users...
    </div>

    <!-- Users Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <UserCard
          v-for="user in users"
          :key="user.id"
          :user="user"
          @edit="openEditModal"
          @delete="openDeleteModal"
      />
    </div>

    <!-- Edit User Modal -->
    <EditUserModal
        v-if="isEditOpen && editUser"
        :isOpen="isEditOpen"
        :user="editUser"
        @close="isEditOpen = false"
        @updated="updateUser"
    />

    <!-- Delete User Modal -->
    <DeleteUserModal
        v-if="isDeleteOpen && deleteUserId"
        :isOpen="isDeleteOpen"
        :userId="deleteUserId"
        @close="isDeleteOpen = false"
        @deleted="removeUser"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Loader2 } from "lucide-vue-next";
import UserCard from "../users/userCard.vue";
import EditUserModal from "../users/modals/EditUserModal.vue";
import DeleteUserModal from "../users/modals/DeleteUserModal.vue";
import api from "../../utils/api.ts";

const users = ref<any[]>([]);
const loading = ref(true);

// Edit Modal State
const isEditOpen = ref(false);
const editUser = ref<any | null>(null);

// Delete Modal State
const isDeleteOpen = ref(false);
const deleteUserId = ref<number | null>(null);

// Fetch Users from API
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

const openEditModal = (user) => {
  if (!user || !user.id) {
    console.error("❌ Invalid user selected:", user);
    return;
  }

  console.log("📝 Editing User:", user); // Debugging log

  editUser.value = user; // Store the full user object
  isEditOpen.value = true; // Open the modal
};


// Open Delete Modal
const openDeleteModal = (userId: number) => {
  deleteUserId.value = userId;
  isDeleteOpen.value = true;
};

// Update User in List after Edit
const updateUser = (updatedUser: any) => {
  const index = users.value.findIndex((u) => u.id === updatedUser.id);
  if (index !== -1) {
    users.value[index] = updatedUser;
  }
  isEditOpen.value = false;
};

// Remove User from List after Deletion
const removeUser = (userId: number) => {
  users.value = users.value.filter((user) => user.id !== userId);
  isDeleteOpen.value = false;
};

onMounted(fetchUsers);
</script>
