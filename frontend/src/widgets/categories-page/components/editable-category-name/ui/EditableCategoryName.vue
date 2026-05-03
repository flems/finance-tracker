<template>
  <div class="flex items-center gap-1.5 min-w-0">
    <template v-if="isEditing">
      <input
        ref="inputRef"
        v-model="editValue"
        type="text"
        class="flex-1 min-w-0 px-2 py-0.5 text-sm font-medium text-gray-900 border border-blue-400 rounded outline-none focus:ring-2 focus:ring-blue-300"
        @keydown.enter="save"
        @keydown.escape="cancel"
        @blur="save"
      />
      <button
        :disabled="isSaving"
        class="flex-shrink-0 p-1 rounded text-blue-600 hover:text-blue-800 hover:bg-blue-50 disabled:opacity-40 transition-colors"
        title="Сохранить"
        @click="save"
      >
        <svg
          v-if="!isSaving"
          xmlns="http://www.w3.org/2000/svg"
          class="w-4 h-4"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
            clip-rule="evenodd"
          />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          class="w-4 h-4 animate-spin"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
        </svg>
      </button>
    </template>

    <span
      v-else
      class="block w-full truncate cursor-pointer select-none"
      title="Двойной клик для редактирования"
      @dblclick="startEdit"
      >{{ name }}</span
    >
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref } from 'vue'
import { toast } from 'vue-sonner'
import { editBudgetCategoryName } from '../api/editBudgetCategoryName'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'

const props = defineProps<{
  id: number
  name: string
}>()

const emit = defineEmits<{
  updated: [category: BudgetCategory]
}>()

const isEditing = ref(false)
const isSaving = ref(false)
const isCancelling = ref(false)
const editValue = ref('')
const inputRef = ref<HTMLInputElement | null>(null)

function startEdit() {
  editValue.value = props.name
  isCancelling.value = false
  isEditing.value = true
  nextTick(() => {
    inputRef.value?.focus()
    inputRef.value?.select()
  })
}

function cancel() {
  isCancelling.value = true
  isEditing.value = false
}

async function save() {
  if (isSaving.value || isCancelling.value) return
  const trimmed = editValue.value.trim()
  if (!trimmed || trimmed === props.name) {
    cancel()
    return
  }

  isSaving.value = true
  try {
    const updated = await editBudgetCategoryName(props.id, trimmed)
    emit('updated', updated)
    isEditing.value = false
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Не удалось сохранить название')
  } finally {
    isSaving.value = false
  }
}
</script>
