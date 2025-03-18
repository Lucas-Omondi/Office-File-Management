<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" class="relative z-50" @close="closeModal">
      <div class="fixed inset-0 bg-black bg-opacity-50"></div>

      <div class="fixed inset-0 flex items-center justify-center">
        <DialogPanel class="w-full max-w-sm p-6 bg-white rounded-lg shadow-xl">
          <DialogTitle class="text-xl font-semibold text-gray-800">Delete User</DialogTitle>
          <p class="mt-3 text-gray-600">Are you sure you want to delete this user? This action cannot be undone.</p>

          <!-- Buttons -->
          <div class="mt-5 flex justify-end gap-3">
            <button @click="closeModal" class="px-4 py-2 text-gray-600 border rounded">Cancel</button>
            <button @click="confirmDelete" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
              Delete
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import { Dialog, DialogPanel, DialogTitle, TransitionRoot } from "@headlessui/vue";
import api from "../../../utils/api.ts";

const props = defineProps<{ isOpen: boolean; userId: number }>();
const emit = defineEmits(["close", "deleted"]);

const closeModal = () => emit("close");

const confirmDelete = async () => {
  try {
    await api.delete(`users/${props.userId}/`);
    emit("deleted", props.userId);
    closeModal();
  } catch (error) {
    console.error("❌ Error deleting user:", error);
  }
};
</script>
