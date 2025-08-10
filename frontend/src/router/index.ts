import { createRouter, createWebHistory } from 'vue-router'
const HomePage = () => import('../pages/HomePage.vue')
const DocsPage = () => import('../pages/DocsPage.vue')
const LoginPage = () => import('../pages/LoginPage.vue')
const VotePage = () => import('../pages/VotePage.vue')
const DownloadsPage = () => import('../pages/DownloadsPage.vue')

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/docs',
    name: 'DocsPage',
    component: DocsPage,
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
  },
  {
    path: '/vote',
    name: 'VotePage',
    component: VotePage,
  },
  {
    path: '/downloads',
    name: 'DownloadsPage',
    component: DownloadsPage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
