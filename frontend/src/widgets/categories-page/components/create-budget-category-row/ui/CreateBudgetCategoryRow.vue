<template>
  <tr v-if="!isAdding" class="border-t border-gray-200">
    <td colspan="3" class="pt-2">
      <button
        class="flex items-center gap-1.5 text-sm text-gray-400 hover:text-blue-600 transition-colors py-1.5"
        @click="startAdd"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Добавить
      </button>
    </td>
  </tr>

  <tr v-else class="h-11 border-t border-gray-200">
    <td class="pr-2">
      <input
        ref="nameRef"
        v-model="form.name"
        type="text"
        placeholder="Название"
        class="w-full px-2 py-0.5 text-sm border rounded outline-none focus:ring-2 focus:ring-blue-300"
        :class="errors.name ? 'border-red-400 focus:ring-red-200' : 'border-blue-400'"
        @keydown.enter="save"
        @keydown.escape="cancel"
      />
    </td>
    <td class="pr-2">
      <input
        v-model="form.type"
        type="text"
        placeholder="Тип"
        class="w-full px-2 py-0.5 text-sm border rounded outline-none focus:ring-2 focus:ring-blue-300"
        :class="errors.type ? 'border-red-400 focus:ring-red-200' : 'border-blue-400'"
        @input="sanitizeType"
        @keydown.enter="save"
        @keydown.escape="cancel"
      />
    </td>
    <td>
      <div class="flex items-center justify-end gap-1.5">
        <input
          v-model="form.base_amount"
          type="number"
          min="0"
          placeholder="Сумма"
          class="min-w-0 flex-1 px-2 py-0.5 text-sm text-right border border-blue-400 rounded outline-none focus:ring-2 focus:ring-blue-300"
          @keydown.enter="save"
          @keydown.escape="cancel"
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
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            class="w-4 h-4 animate-spin"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
          </svg>
        </button>
      </div>
    </td>
  </tr>
</template>

<script setup lang="ts">
import { nextTick, reactive, ref } from 'vue'
import { toast } from 'vue-sonner'
import { createBudgetCategory } from '../api/createBudgetCategory'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'

const emit = defineEmits<{
  created: [category: BudgetCategory]
}>()

const isAdding = ref(false)
const isSaving = ref(false)
const nameRef = ref<HTMLInputElement | null>(null)

const form = reactive({ name: '', type: '', base_amount: '' })
const errors = reactive({ name: false, type: false })

function sanitizeType(e: Event) {
  const input = e.target as HTMLInputElement
  const cleaned = input.value.replace(/[^a-zA-Z0-9]/g, '')
  form.type = cleaned
  input.value = cleaned
}

function startAdd() {
  form.name = ''
  form.type = ''
  form.base_amount = ''
  errors.name = false
  errors.type = false
  isAdding.value = true
  nextTick(() => nameRef.value?.focus())
}

function cancel() {
  isAdding.value = false
}

function validate(): boolean {
  errors.name = !form.name.trim()
  errors.type = !form.type.trim()
  return !errors.name && !errors.type
}

async function save() {
  if (isSaving.value) return
  if (!validate()) return

  isSaving.value = true
  try {
    const created = await createBudgetCategory({
      name: form.name.trim(),
      type: form.type.trim(),
      base_amount: form.base_amount !== '' ? Number(form.base_amount) : null,
    })
    emit('created', created)
    isAdding.value = false
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Не удалось создать категорию')
  } finally {
    isSaving.value = false
  }
}
</script>
