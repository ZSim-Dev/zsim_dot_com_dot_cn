import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import DocsView from '../components/DocsView.vue';
import LoginView from '../components/LoginView.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/docs',
    name: 'DocsView',
    component: DocsView
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView
  },
  // 其他路由...
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;