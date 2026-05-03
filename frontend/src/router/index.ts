import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/pages/AppLayout.vue'
import BudgetPage from '@/pages/budget/BudgetPage.vue'
import CategoriesPage from '@/pages/categories/CategoriesPage.vue'
import SavingsPage from '@/pages/savings/SavingsPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/budget',
    },
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: 'budget',
          name: 'budget',
          component: BudgetPage,
        },
        {
          path: 'categories',
          name: 'categories',
          component: CategoriesPage,
        },
        {
          path: 'savings',
          name: 'savings',
          component: SavingsPage,
        },
        // редиректы со старых урлов finance-2
        { path: 'finance-2/budget', redirect: '/budget' },
        { path: 'finance-2/categories', redirect: '/categories' },
        { path: 'finance-2/savings', redirect: '/savings' },
        { path: 'finance-2', redirect: '/budget' },
      ],
    },
  ],
})

export default router
