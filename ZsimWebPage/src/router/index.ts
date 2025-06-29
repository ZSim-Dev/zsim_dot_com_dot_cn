import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import DocsView from '../components/DocsView.vue';
import LoginView from '../components/LoginView.vue';
import VoteView from '../components/VoteView.vue';

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
  {
    path: '/vote',
    name: 'VoteView',
    component: VoteView
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;