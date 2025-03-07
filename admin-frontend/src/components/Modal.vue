<script setup lang="ts">
defineProps<{
  title: string;
  show: boolean;
  onClose: () => void;
}>();
</script>

<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-1/3">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">{{ title }}</h2>
        <button @click="onClose" class="text-gray-500 hover:text-red-500">✖</button>
      </div>
      <slot></slot> <!-- Slot for content inside modal -->
    </div>
  </div>
</template>
