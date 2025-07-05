import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import TodayPictureView from "@/views/TodayPictureView.vue";
import TrendingView from "@/views/TrendingView.vue";
import LogInView from "@/views/LogInView.vue";
import SignUpView from "@/views/SignUpView.vue";
import FavouritesView from "@/views/FavouritesView.vue";
import ResetPasswordView from "@/views/ResetPasswordView.vue";
import ResetPasswordConfirmationView from "@/views/ResetPasswordConfirmationView.vue";
import ActivateAccountView from "@/views/ActivateAccountView.vue";
import AboutView from "@/views/AboutView.vue";
import ContributeView from "@/views/ContributeView.vue";
import NotFoundView from "@/views/NotFoundView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/today",
    name: "today",
    component: TodayPictureView,
  },
  {
    path: "/trending",
    name: "trending",
    component: TrendingView,
  },
  {
    path: "/login",
    name: "login",
    component: LogInView,
  },
  {
    path: "/signup",
    name: "signup",
    component: SignUpView,
  },
  {
    path: "/favourites",
    name: "favourites",
    component: FavouritesView,
  },
  {
    path: "/reset_password",
    name: "resetpassword",
    component: ResetPasswordView,
  },
  {
    path: "/activate/:uid/:token",
    name: "activate",
    component: ActivateAccountView,
  },
  {
    path: "/password/reset/confirm/:uid/:token",
    name: "reset_password_confirm",
    component: ResetPasswordConfirmationView,
  },
  {
    path: "/about",
    name: "about",
    component: AboutView,
  },
  {
    path: "/contribute",
    name: "contribute",
    component: ContributeView,
  },
  {
    path: "/:catchAll(.*)",
    name: "notfound",
    component: NotFoundView,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
