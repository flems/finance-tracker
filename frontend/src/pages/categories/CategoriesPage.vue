<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold mb-2">Категории трат</h1>
      <p class="text-gray-600 text-sm">
        Справочник категорий для распределения выплат и базовых сумм
      </p>
    </div>

    <CategoriesPageWidget />
  </div>
</template>

<script setup lang="ts">
import CategoriesPageWidget from '@/widgets/categories-page/index.vue'
</script>
