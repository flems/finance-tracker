<template>
  <table class="w-full text-sm table-fixed">
    <colgroup>
      <col class="w-1/2" />
      <col class="w-1/4" />
      <col class="w-1/4" />
    </colgroup>
    <thead>
      <tr class="border-b border-gray-200 text-left text-gray-500 text-xs uppercase tracking-wide">
        <th class="pb-3 pl-3 pr-4 font-medium">Название</th>
        <th class="pb-3 pr-4 font-medium">Тип</th>
        <th class="pb-3 pr-3 font-medium text-right">Базовая сумма</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-100">
      <tr
        v-for="category in categories"
        :key="category.id"
        class="group relative h-11 transition-colors"
        :style="category.color ? { backgroundColor: category.color + '18' } : {}"
        :class="!category.color ? 'hover:bg-gray-50' : ''"
      >
        <td
          class="pl-3 pr-4 font-medium text-gray-900 border-l-4 transition-colors"
          :style="category.color ? { borderColor: category.color } : {}"
          :class="!category.color ? 'border-transparent' : ''"
        >
          <div class="flex items-center gap-2">
            <slot name="color" :category="category" />
            <slot name="name" :category="category">{{ category.name }}</slot>
          </div>
        </td>
        <td class="pr-4 text-gray-500">{{ category.type ?? '—' }}</td>
        <td class="relative pr-3 text-right text-gray-700">
          <slot name="base_amount" :category="category">
            {{
              category.base_amount != null
                ? category.base_amount.toLocaleString('ru-RU') + ' ₽'
                : '—'
            }}
          </slot>
          <span
            class="absolute -right-7 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <slot name="actions" :category="category" />
          </span>
        </td>
      </tr>
    </tbody>
    <tfoot>
      <slot name="footer" />
    </tfoot>
  </table>
</template>

<script setup lang="ts">
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'

defineProps<{
  categories: BudgetCategory[]
}>()
</script>
