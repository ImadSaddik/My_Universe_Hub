import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    isAuthenticated: false,
    token: localStorage.getItem('token') || '',
    username: localStorage.getItem('username') || ''
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
    setUsername (state, username) {
      state.username = username
    },
    removeUsername (state) {
      state.username = ''
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
