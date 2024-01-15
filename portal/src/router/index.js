import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue')
    },
    {
      path: '/services',
      component: () => import('../views/services/ServicesView.vue'),
    },
    {
      path: '/services/:id',
      name: 'services.show',
      component: () => import('../views/services/Show.vue'),
    },
    {
      path: '/services/:id/service_requests/new',
      name: 'service_requests.new',
      component: () => import('../views/service_requests/New.vue'),
      beforeEnter: (to, _from) => {
        const authStore = useAuthStore();

        if (!authStore.isLoggedIn && to.name !== 'login') {
          return { name: 'login' }
        }
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue')
    },
    {
      path: '/register/:id',
      name: 'registerUniqueLink',
      component: () => import('../views/auth/RegisterUniqueLinkView.vue')
    },
    {
      path: '/requests',
      name: 'requests',
      component: () => import('../views/requests/RequestsView.vue'),
      beforeEnter: (to, _from) => {
        const authStore = useAuthStore();

        if (!authStore.isLoggedIn && to.name !== 'login') {
          return { name: 'login' }
        }
      }
    },
    {
      path: '/requests/:id',
      name: 'request-show',
      component: () => import('../views/requests/RequestsShowView.vue'),
      beforeEnter: (to, _from) => {
        const authStore = useAuthStore();

        if (!authStore.isLoggedIn && to.name !== 'login') {
          return { name: 'login' }
        }
      }
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: () => import('../views/statistics/StatisticsView.vue')
    },
  ]
})

export default router
