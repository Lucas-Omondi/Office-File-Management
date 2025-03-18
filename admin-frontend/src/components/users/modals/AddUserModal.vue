<script setup lang="ts">
import { ref, watch } from "vue";
import { Dialog, DialogPanel, DialogTitle, TransitionRoot } from "@headlessui/vue";
import { useMotion } from "@vueuse/motion";
import api from "../../../utils/api.ts";

const props = defineProps<{ isOpen: boolean }>();
const emit = defineEmits(["close", "added"]);

// Form Data
const form = ref({
  username: "",
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  role: "Basic",
});
const loading = ref(false);
const errorMessage = ref("");

// Watch for Modal Open & Reset Form
watch(
    () => props.isOpen,
    (open) => {
      if (open) {
        form.value = { username: "", first_name: "", last_name: "", email: "", password:"", role: "Basic" };
        errorMessage.value = "";
      }
    }
);

// Add User Function
const addUser = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    const response = await api.post("users/", form.value);
    emit("added", response.data); // Send new user data to parent
    closeModal();
  } catch (error) {
    console.error("❌ Error adding user:", error);
    errorMessage.value = "Failed to add user. Please try again.";
  } finally {
    loading.value = false;
  }
};

// Close Modal
const closeModal = () => emit("close");

// Motion Animation
const modalRef = ref(null);
useMotion(modalRef, {
  initial: { opacity: 0, y: 20 },
  enter: { opacity: 1, y: 0, transition: { duration: 0.3 } },
  leave: { opacity: 0, y: 20, transition: { duration: 0.2 } },
});
</script>

<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" class="relative z-50" @close="closeModal">
      <div class="fixed inset-0 bg-black/30 backdrop-blur-md"></div>
      <div class="fixed inset-0 flex items-center justify-center p-4">
        <DialogPanel ref="modalRef" class="w-full max-w-md p-6 bg-white rounded-lg shadow-xl">
          <DialogTitle class="text-xl font-semibold text-gray-800">Add New User</DialogTitle>

          <!-- Error Message -->
          <p v-if="errorMessage" class="mt-2 text-red-500 text-sm">{{ errorMessage }}</p>

          <!-- User Form -->
          <div class="mt-4 space-y-3">
            <label class="block text-gray-700">Username</label>
            <input v-model="form.username" type="text" class="w-full p-2 border rounded" placeholder="Enter username">

            <label class="block text-gray-700">First Name</label>
            <input v-model="form.first_name" type="text" class="w-full p-2 border rounded" placeholder="Enter first name">

            <label class="block text-gray-700">Last Name</label>
            <input v-model="form.last_name" type="text" class="w-full p-2 border rounded" placeholder="Enter last name">

            <label class="block text-gray-700">Email</label>
            <input v-model="form.email" type="email" class="w-full p-2 border rounded" placeholder="Enter email">

            <label class="block text-gray-700">Password</label>
            <input v-model="form.password" type="password" class="w-full p-2 border rounded" placeholder="Enter password">


            <label class="block text-gray-700">Role</label>
            <select v-model="form.role" class="w-full p-2 border rounded">
              <option value="Basic">Basic User</option>
              <option value="Admin">Admin</option>
              <option value="Super admin">Super Admin</option>
            </select>
          </div>

          <!-- Buttons -->
          <div class="mt-5 flex justify-end gap-3">
            <button @click="closeModal" class="px-4 py-2 text-gray-600 border rounded hover:bg-gray-100">
              Cancel
            </button>
            <button
                @click="addUser"
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center"
                :disabled="loading"
            >
              <svg v-if="loading" class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
              </svg>
              {{ loading ? "Adding..." : "Add User" }}
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
