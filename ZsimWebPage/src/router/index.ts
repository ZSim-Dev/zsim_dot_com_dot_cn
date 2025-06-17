import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import DocsView from '../components/DocsView.vue'; // 文档视图

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
  // 其他路由...
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;