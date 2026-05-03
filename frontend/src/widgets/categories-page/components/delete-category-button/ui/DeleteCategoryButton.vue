<template>
  <button
    :disabled="isDeleting"
    class="p-1 rounded text-gray-300 hover:text-red-500 hover:bg-red-50 disabled:opacity-40 transition-colors"
    title="Удалить категорию"
    @click.stop="handleDelete"
  >
    <svg
      v-if="!isDeleting"
      xmlns="http://www.w3.org/2000/svg"
      class="w-4 h-4"
      viewBox="0 0 20 20"
      fill="currentColor"
    >
      <path
        fill-rule="evenodd"
        d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
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
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
    </svg>
  </button>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { toast } from 'vue-sonner'
import { deleteBudgetCategory } from '../api/deleteBudgetCategory'

const props = defineProps<{ id: number }>()

const emit = defineEmits<{
  deleted: [id: number]
}>()

const isDeleting = ref(false)

async function handleDelete() {
  if (isDeleting.value) return
  isDeleting.value = true
  try {
    await deleteBudgetCategory(props.id)
    emit('deleted', props.id)
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Не удалось удалить категорию')
  } finally {
    isDeleting.value = false
  }
}
</script>
