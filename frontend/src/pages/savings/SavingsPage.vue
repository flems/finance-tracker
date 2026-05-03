<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold mb-2">Накопления</h1>
      <p class="text-gray-600 text-sm">Цели, прогресс и история пополнений</p>
    </div>

    <SavingsPageWidget />
  </div>
</template>

<script setup lang="ts">
import SavingsPageWidget from '@/widgets/savings-page/index.vue'
</script>
