<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold mb-2">Бюджет</h1>
      <p class="text-gray-600 text-sm">
        Сколько и куда ушло с каждого дохода. Добавляйте выплаты, распределяйте суммы по категориям и отмечайте что уже оплачено.
      </p>
    </div>

    <BudgetPageWidget />
  </div>
</template>

<script setup lang="ts">
import BudgetPageWidget from '@/widgets/budget-page/index.vue'
</script>
