import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    isAuthenticated: false,
    token: localStorage.getItem('token') || '',
    email: localStorage.getItem('email') || '',
    selectedNavbarItem: localStorage.getItem('selectedNavbarItem') || ''
  },
  getters: {
  },
  mutations: {
    setToken (state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    removeToken (state) {
      state.token = ''
      state.isAuthenticated = false
    },
    setEmail (state, email) {
      state.email = email
    },
    removeEmail (state) {
      state.email = ''
    },
    setSelectedNavbarItem (state, selectedNavbarItem) {
      state.selectedNavbarItem = selectedNavbarItem
    }
  },
  actions: {
    login ({ commit }, token) {
      commit('setToken', token)
      axios.defaults.headers.common.Authorization = 'Token ' + token
      localStorage.setItem('token', token)
    }
  },
  modules: {
  }
})
