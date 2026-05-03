<template>
  <button
    type="button"
    class="p-1 rounded text-gray-300 hover:text-red-500 hover:bg-red-50 transition-colors"
    title="Удалить цель"
    @click="modalOpen = true"
  >
    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
      <path
        fill-rule="evenodd"
        d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
        clip-rule="evenodd"
      />
    </svg>
  </button>

  <ConfirmModal
    v-model="modalOpen"
    title="Удалить цель?"
    :description="`Цель «${goalTitle}» и все связанные данные будут удалены безвозвратно.`"
    confirm-label="Удалить"
    cancel-label="Отмена"
    :loading="isDeleting"
    @confirm="handleDelete"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { toast } from 'vue-sonner'
import ConfirmModal from '@/shared/ui/confirm-modal/ConfirmModal.vue'
import { HttpError } from '@/shared/api/http'
import { deleteSavingGoal } from '../api/deleteSavingGoal'

const props = defineProps<{ goalId: number; goalTitle: string }>()
const emit = defineEmits<{ deleted: [goalId: number] }>()

const modalOpen = ref(false)
const isDeleting = ref(false)

async function handleDelete() {
  isDeleting.value = true
  try {
    await deleteSavingGoal(props.goalId)
    modalOpen.value = false
    emit('deleted', props.goalId)
  } catch (e) {
    toast.error(e instanceof HttpError ? e.message : 'Не удалось удалить цель')
  } finally {
    isDeleting.value = false
  }
}
</script>
