<script setup lang="ts">
defineProps(["confirm", "cancel"]);
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded-lg shadow-xl w-96">
      <h2 class="text-lg font-semibold text-gray-800">Confirm Deletion</h2>
      <p class="text-gray-600 my-4">Are you sure you want to delete the selected projects?</p>
      <div class="flex justify-end gap-3">
        <button @click="$emit('cancel')" class="bg-gray-400 hover:bg-gray-500 text-white px-4 py-2 rounded">Cancel</button>
        <button @click="$emit('confirm')" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded">Delete</button>
      </div>
    </div>
  </div>
</template>

