<template>
  <div class="bg-white rounded-lg shadow p-6 space-y-4">
    <h2 class="text-xl font-semibold text-gray-900">Категории Бюджета</h2>

    <div v-if="isLoading" class="flex items-center justify-center py-8 text-gray-400">
      Загрузка...
    </div>

    <div v-else-if="error" class="text-red-500 text-sm py-4">
      {{ error }}
    </div>

    <div v-else class="overflow-x-auto overflow-y-visible pr-8">
      <BudgetCategoryTable :categories="categories">
        <template #color="{ category }">
          <CategoryColorPicker
            :id="category.id"
            :color="category.color"
            @updated="onCategoryUpdated"
          />
        </template>
        <template #name="{ category }">
          <EditableCategoryName
            :id="category.id"
            :name="category.name"
            @updated="onCategoryUpdated"
          />
        </template>
        <template #base_amount="{ category }">
          <EditableCategoryBaseAmount
            :id="category.id"
            :base-amount="category.base_amount"
            @updated="onCategoryUpdated"
          />
        </template>
        <template #actions="{ category }">
          <DeleteCategoryButton :id="category.id" @deleted="onCategoryDeleted" />
        </template>
        <template #footer>
          <CreateBudgetCategoryRow @created="onCategoryCreated" />
        </template>
      </BudgetCategoryTable>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchBudgetCategories, type BudgetCategory } from '@/entities/budget-category/api/budgetCategoryApi'
import BudgetCategoryTable from '@/entities/budget-category/ui/BudgetCategoryTable.vue'
import EditableCategoryName from './components/editable-category-name/ui/EditableCategoryName.vue'
import EditableCategoryBaseAmount from './components/editable-category-base-amount/ui/EditableCategoryBaseAmount.vue'
import CreateBudgetCategoryRow from './components/create-budget-category-row/ui/CreateBudgetCategoryRow.vue'
import DeleteCategoryButton from './components/delete-category-button/ui/DeleteCategoryButton.vue'
import CategoryColorPicker from './components/category-color-picker/ui/CategoryColorPicker.vue'

const categories = ref<BudgetCategory[]>([])
const isLoading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  isLoading.value = true
  error.value = null
  try {
    categories.value = await fetchBudgetCategories()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Неизвестная ошибка'
  } finally {
    isLoading.value = false
  }
})

function onCategoryUpdated(updated: BudgetCategory) {
  const idx = categories.value.findIndex(c => c.id === updated.id)
  if (idx !== -1) {
    categories.value[idx] = updated
  }
}

function onCategoryCreated(created: BudgetCategory) {
  categories.value.push(created)
}

function onCategoryDeleted(id: number) {
  categories.value = categories.value.filter(c => c.id !== id)
}
</script>
