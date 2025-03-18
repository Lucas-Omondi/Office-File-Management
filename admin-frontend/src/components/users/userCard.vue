<template>
  <div
      class="relative p-5 bg-white/70 backdrop-blur-md shadow-lg rounded-xl border border-gray-200 transition transform hover:scale-105"
  >
    <!-- Profile Section -->
    <div class="flex items-center space-x-4">
      <div
          class="w-12 h-12 rounded-full bg-gray-300 flex items-center justify-center text-xl font-semibold text-gray-700"
      >
        {{ user.first_name?.charAt(0) || "" }}{{ user.last_name?.charAt(0) || "" }}
      </div>
      <div>
        <h2 class="text-lg font-semibold text-gray-800">
          {{ user.first_name || "Unknown" }} {{ user.last_name || "" }}
        </h2>
        <p class="text-sm text-gray-500">{{ user.email || "No email provided" }}</p>
      </div>
    </div>

    <!-- Role & Status -->
    <div class="mt-3 flex gap-2">
      <span
          class="px-3 py-1 text-sm rounded-full font-medium"
          :class="user.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
      >
        {{ user.is_active ? "Active" : "Inactive" }}
      </span>
      <span class="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-full capitalize">
        {{ user.role }}
      </span>
    </div>

    <!-- Actions -->
    <div class="mt-4 flex justify-between">
      <button
          @click="$emit('edit', user)"
          class="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 transition"
      >
        Edit
      </button>
      <button
          @click="$emit('delete', user.id)"
          class="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600 transition"
      >
        Delete
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ user: any }>();
defineEmits(["edit", "delete"]);
</script>
