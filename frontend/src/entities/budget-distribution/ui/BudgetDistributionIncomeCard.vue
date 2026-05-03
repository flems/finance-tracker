<template>
  <div>
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-xl font-semibold">
        Распределение зп {{ formatShortDate(income.payout_date) }}
        <span class="font-normal text-gray-500">— {{ formatAmount(income.amount) }}</span>
      </h2>
      <slot name="income-actions" />
    </div>

    <div class="bg-white rounded-lg shadow">
      <div>
        <table class="w-full table-fixed">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-[38%]">
                Категория
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-[22%]">
                Сумма (₽)
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Комментарий
              </th>
              <th class="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-12" />
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="!income.items.length">
              <td colspan="4" class="px-6 py-6 text-sm text-gray-400 text-center">
                Нет строк — нажмите «Добавить» ниже
              </td>
            </tr>
            <template v-for="item in income.items" :key="item.id">
              <slot name="item-row" :item="item" />
            </template>
            <slot name="footer" />
            <tr class="bg-gray-50 font-semibold">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">ИТОГО</td>
              <td class="px-6 py-4 text-sm" :class="totalColorClass(income)">
                {{ formatAmount(allocated(income)) }}
              </td>
              <td class="px-6 py-4 text-sm" :class="totalColorClass(income)">
                {{ totalComment(income) }}
              </td>
              <td class="px-2 py-4" />
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { BudgetDistributionIncome } from '../api/budgetDistributionApi'
import { allocated, formatAmount, formatShortDate, totalColorClass, totalComment } from '../lib/formatters'

defineProps<{
  income: BudgetDistributionIncome
}>()
</script>
