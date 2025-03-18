<script setup lang="ts">
defineProps<{
  title: string;
  message: string;
  visible: boolean;
  confirm: () => void;
  cancel: () => void;
}>();
</script>

<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
    <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg w-96">
      <h2 class="text-lg font-semibold">{{ title }}</h2>
      <p class="mt-2 text-gray-600 dark:text-gray-300">{{ message }}</p>
      <div class="mt-4 flex justify-end gap-2">
        <button @click="cancel" class="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded-md">Cancel</button>
        <button @click="confirm" class="px-4 py-2 bg-red-600 text-white rounded-md">Confirm</button>
      </div>
    </div>
  </div>
</template>
