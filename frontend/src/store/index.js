import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state: {
    userVisitedTheWebsite: false,
    apodStatus: "checking",
    isAuthenticated: false,
    token: localStorage.getItem("token") || "",
    email: localStorage.getItem("email") || "",
    selectedNavbarItem: localStorage.getItem("selectedNavbarItem") || "",
    errorMessages: [
      // {
      //   id: Date.now() + Math.random(),
      //   message: "The backend is not responding. Please try again later. Please try again later Please try again later",
      // },
      // {
      //   id: Date.now() + Math.random(),
      //   message: "Another error.",
      // },
    ],
  },
  getters: {},
  mutations: {
    setToken(state, token) {
      state.token = token;
      state.isAuthenticated = true;
    },
    removeToken(state) {
      state.token = "";
      state.isAuthenticated = false;
    },
    setEmail(state, email) {
      state.email = email;
    },
    removeEmail(state) {
      state.email = "";
    },
    setSelectedNavbarItem(state, selectedNavbarItem) {
      state.selectedNavbarItem = selectedNavbarItem;
    },
    setApodStatus(state, status) {
      state.apodStatus = status;
    },
    setUserVisitedTheWebsite(state, visited) {
      state.userVisitedTheWebsite = visited;
    },
    addErrorMessage(state, message) {
      state.errorMessages = [...state.errorMessages, { id: Date.now() + Math.random(), message }];
    },
    removeErrorMessage(state, id) {
      state.errorMessages = state.errorMessages.filter((error) => error.id !== id);
    },
  },
  actions: {
    login({ commit }, token) {
      commit("setToken", token);
      axios.defaults.headers.common.Authorization = "Token " + token;
      localStorage.setItem("token", token);
    },
  },
  modules: {},
});
