<template>
  <header class="bg-white shadow-sm">
    <div class="container mx-auto px-4">
      <nav class="flex gap-4 py-3">
        <router-link
          v-for="link in links"
          :key="link.path"
          :to="link.path"
          class="px-4 py-2 rounded-md text-gray-700 hover:bg-gray-100 transition-colors text-sm"
          :class="{ 'bg-blue-100 text-blue-700': isLinkActive(link) }"
        >
          {{ link.label }}
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

const links = [
  { path: '/budget', label: 'Бюджет' },
  { path: '/categories', label: 'Категории трат' },
  { path: '/savings', label: 'Накопления' },
]

function isLinkActive(link: { path: string }): boolean {
  return route.path === link.path
}
</script>
