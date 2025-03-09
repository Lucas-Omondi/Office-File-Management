<script setup lang="ts">
import { defineProps, defineEmits } from "vue";

defineProps<{ show: boolean }>();
defineEmits(["close"]);
</script>

<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-1/3 transition-all duration-300 transform scale-95">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">New Project</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-red-500 text-2xl">✖</button>
      </div>
      <slot></slot> <!-- Injects forms dynamically -->
    </div>
  </div>
</template>
