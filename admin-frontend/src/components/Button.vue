<script setup lang="ts">
defineProps<{
  label: string;
  icon?: string;
  color?: "green" | "blue" | "red"; // Default color options
  onClick: () => void;
}>();
</script>

<template>
  <button
      @click="onClick"
      :class="[
      'flex items-center gap-2 px-4 py-2 rounded-lg text-white shadow-md transition-all duration-200',
      color === 'green' ? 'bg-green-600 hover:bg-green-700' :
      color === 'blue' ? 'bg-blue-600 hover:bg-blue-700' :
      color === 'red' ? 'bg-red-600 hover:bg-red-700' : 'bg-gray-600 hover:bg-gray-700'
    ]"
  >
    <i v-if="icon" :class="icon"></i>
    {{ label }}
  </button>
</template>
