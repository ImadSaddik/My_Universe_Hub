import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TodayPictureView from '../views/TodayPictureView.vue'
import TrendingView from '../views/TrendingView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/today',
    name: 'today',
    component: TodayPictureView
  },
  {
    path: '/trending',
    name: 'trending',
    component: TrendingView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
