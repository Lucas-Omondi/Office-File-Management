<script setup lang="ts">
import { ref, watch } from "vue";
import { Dialog, DialogPanel, DialogTitle, TransitionRoot } from "@headlessui/vue";
import { useMotion } from "@vueuse/motion";
import api from "../../../utils/api.ts";

const props = defineProps<{ isOpen: boolean; user: any | null }>();
const emit = defineEmits(["close", "updated"]);

const form = ref({
  first_name: "",
  last_name: "",
  email: "",
  role: "basic_user",
});

const loading = ref(false);
const modalRef = ref(null);

// Smooth animation using VueUse Motion
useMotion(modalRef, {
  initial: { opacity: 0, y: 20 },
  enter: { opacity: 1, y: 0, transition: { duration: 0.3 } },
  leave: { opacity: 0, y: 10, transition: { duration: 0.2 } },
});

// Watch for Modal Open and Populate Form
watch(
    () => props.user,
    (newUser) => {
      if (newUser) form.value = { ...newUser };
    },
    { deep: true, immediate: true }
);

// Close Modal
const closeModal = () => emit("close");

// Save Changes
const saveChanges = async () => {
  if (!props.user) return;
  loading.value = true;
  try {
    await api.patch(`users/${props.user.id}/`, form.value);
    emit("updated", { ...props.user, ...form.value });
    closeModal();
  } catch (error) {
    console.error("❌ Error updating user:", error);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" class="relative z-50" @close="closeModal">
      <!-- Backdrop Blur & Opacity -->
      <div class="fixed inset-0 bg-black/40 backdrop-blur-md"></div>

      <div class="fixed inset-0 flex items-center justify-center">
        <DialogPanel
            ref="modalRef"
            class="w-full max-w-md p-6 bg-white rounded-lg shadow-2xl border border-gray-200"
        >
          <!-- Title -->
          <DialogTitle class="text-xl font-semibold text-gray-900 mb-4">Edit User</DialogTitle>

          <!-- User Form -->
          <div class="space-y-4">
            <div>
              <label class="block text-gray-700 font-medium">First Name</label>
              <input
                  v-model="form.first_name"
                  type="text"
                  class="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-400 transition"
              >
            </div>

            <div>
              <label class="block text-gray-700 font-medium">Last Name</label>
              <input
                  v-model="form.last_name"
                  type="text"
                  class="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-400 transition"
              >
            </div>

            <div>
              <label class="block text-gray-700 font-medium">Email</label>
              <input
                  v-model="form.email"
                  type="email"
                  class="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-400 transition"
              >
            </div>

            <div>
              <label class="block text-gray-700 font-medium">Role</label>
              <select
                  v-model="form.role"
                  class="w-full mt-1 p-2 border rounded-md bg-gray-50 focus:ring-2 focus:ring-blue-400 transition"
              >
                <option value="Basic">Basic User</option>
                <option value="Admin">Admin</option>
                <option value="Super admin">Super Admin</option>
              </select>
            </div>
          </div>

          <!-- Buttons -->
          <div class="mt-5 flex justify-end gap-3">
            <button
                @click="closeModal"
                class="px-4 py-2 text-gray-600 border rounded-md hover:bg-gray-100 transition"
                :disabled="loading"
            >
              Cancel
            </button>
            <button
                @click="saveChanges"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center transition"
                :disabled="loading"
            >
              <svg v-if="loading" class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
              </svg>
              {{ loading ? "Saving..." : "Save" }}
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
