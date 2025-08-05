import { createRouter, createWebHistory } from 'vue-router'
const Home = () => import('../components/Home.vue')
const DocsView = () => import('../components/DocsView.vue')
const LoginView = () => import('../components/LoginView.vue')
const VoteView = () => import('../components/VoteView.vue')
const Downloads = () => import('../components/Downloads.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/docs',
    name: 'DocsView',
    component: DocsView,
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView,
  },
  {
    path: '/vote',
    name: 'VoteView',
    component: VoteView,
  },
  {
    path: '/downloads',
    name: 'Downloads',
    component: Downloads,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
