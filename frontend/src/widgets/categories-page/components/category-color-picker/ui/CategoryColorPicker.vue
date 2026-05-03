<template>
  <div class="relative">
    <button
      class="w-4 h-4 rounded-full border-2 border-white ring-1 ring-gray-200 flex-shrink-0 transition-transform hover:scale-110"
      :style="color ? { backgroundColor: color } : {}"
      :class="!color ? 'bg-gray-200' : ''"
      title="Выбрать цвет"
      @click.stop="isOpen = !isOpen"
    />

    <div
      v-if="isOpen"
      class="absolute left-0 top-6 z-20 bg-white rounded-lg shadow-lg border border-gray-100 p-2 w-40"
    >
      <div class="grid grid-cols-5 gap-1.5">
        <button
          v-for="preset in PRESETS"
          :key="preset"
          class="w-6 h-6 rounded-full border-2 transition-transform hover:scale-110"
          :class="color === preset ? 'border-gray-500' : 'border-white ring-1 ring-gray-200'"
          :style="{ backgroundColor: preset }"
          @click.stop="select(preset)"
        />
      </div>
      <button
        class="mt-2 w-full text-xs text-gray-400 hover:text-gray-600 transition-colors text-center"
        @click.stop="select(null)"
      >
        Сбросить
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { toast } from 'vue-sonner'
import { editBudgetCategoryColor } from '../api/editBudgetCategoryColor'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'

const PRESETS = [
  '#ef4444', '#f97316', '#eab308', '#22c55e', '#10b981',
  '#14b8a6', '#06b6d4', '#3b82f6', '#6366f1', '#8b5cf6',
  '#a855f7', '#ec4899', '#f43f5e', '#64748b', '#78716c',
]

const props = defineProps<{ id: number; color: string | null }>()
const emit = defineEmits<{ updated: [category: BudgetCategory] }>()

const isOpen = ref(false)

async function select(value: string | null) {
  isOpen.value = false
  try {
    const updated = await editBudgetCategoryColor(props.id, value)
    emit('updated', updated)
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Не удалось обновить цвет')
  }
}

function onClickOutside(e: MouseEvent) {
  if (!(e.target as HTMLElement).closest('.relative')) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>
