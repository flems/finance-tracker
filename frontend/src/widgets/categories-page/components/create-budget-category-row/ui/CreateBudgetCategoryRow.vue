<template>
  <tr v-if="!isAdding" class="border-t border-gray-200">
    <td colspan="3" class="pt-2">
      <button
        class="flex items-center gap-1.5 text-sm text-gray-400 hover:text-blue-600 transition-colors py-1.5"
        @click="startAdd"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="w-4 h-4"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
            clip-rule="evenodd"
          />
        </svg>
        Добавить
      </button>
    </td>
  </tr>

  <tr v-else class="h-11 border-t border-gray-200">
    <td
      class="pl-3 pr-4 border-l-4 transition-colors"
      :style="form.color ? { borderColor: form.color } : {}"
      :class="!form.color ? 'border-transparent' : ''"
    >
      <div class="flex items-center gap-2">
        <div class="relative flex-shrink-0">
          <button
            class="w-4 h-4 rounded-full border-2 border-white ring-1 ring-gray-200 transition-transform hover:scale-110"
            :style="form.color ? { backgroundColor: form.color } : {}"
            :class="!form.color ? 'bg-gray-200' : ''"
            title="Выбрать цвет"
            @click.stop="isColorOpen = !isColorOpen"
          />
          <div
            v-if="isColorOpen"
            class="absolute left-0 bottom-6 z-20 bg-white rounded-lg shadow-lg border border-gray-100 p-2 w-40"
          >
            <div class="grid grid-cols-5 gap-1.5">
              <button
                v-for="preset in COLOR_PRESETS"
                :key="preset"
                class="w-6 h-6 rounded-full border-2 transition-transform hover:scale-110"
                :class="
                  form.color === preset ? 'border-gray-500' : 'border-white ring-1 ring-gray-200'
                "
                :style="{ backgroundColor: preset }"
                @click.stop="selectColor(preset)"
              />
            </div>
            <button
              class="mt-2 w-full text-xs text-gray-400 hover:text-gray-600 transition-colors text-center"
              @click.stop="selectColor(null)"
            >
              Сбросить
            </button>
          </div>
        </div>
        <input
          ref="nameRef"
          v-model="form.name"
          type="text"
          placeholder="Название"
          class="min-w-0 flex-1 px-2 py-0.5 text-sm border rounded outline-none focus:ring-2 focus:ring-blue-300"
          :class="errors.name ? 'border-red-400 focus:ring-red-200' : 'border-blue-400'"
          @keydown.enter="save"
          @keydown.escape="cancel"
        />
      </div>
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
      </div>
    </td>
  </tr>
</template>

<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, reactive, ref } from 'vue'
import { toast } from 'vue-sonner'
import { createBudgetCategory } from '../api/createBudgetCategory'
import type { BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'

const COLOR_PRESETS = [
  '#ef4444',
  '#f97316',
  '#eab308',
  '#22c55e',
  '#10b981',
  '#14b8a6',
  '#06b6d4',
  '#3b82f6',
  '#6366f1',
  '#8b5cf6',
  '#a855f7',
  '#ec4899',
  '#f43f5e',
  '#64748b',
  '#78716c',
]

const emit = defineEmits<{
  created: [category: BudgetCategory]
}>()

const isAdding = ref(false)
const isSaving = ref(false)
const isColorOpen = ref(false)
const nameRef = ref<HTMLInputElement | null>(null)

const form = reactive({ name: '', type: '', base_amount: '', color: null as string | null })
const errors = reactive({ name: false, type: false })

function onClickOutside(e: MouseEvent) {
  if (!(e.target as HTMLElement).closest('.relative')) {
    isColorOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))

function selectColor(value: string | null) {
  form.color = value
  isColorOpen.value = false
}

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
  form.color = null
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
      color: form.color,
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
