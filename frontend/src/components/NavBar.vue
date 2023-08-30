<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid px-5">
      <RouterLink class="navbar-brand" to="/">
        <img src="../assets/apod_logo.svg" alt="">
      </RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="row w-100 navbar-nav">
          <div class="col d-flex align-items-center">
            <a class="nav-link active" aria-current="page" href="/">Home</a>
            <a class="nav-link" href="/today">Today's picture</a>
            <a class="nav-link" href="/trending">Trending</a>
            <a class="nav-link" href="/favourites">Favourites</a>
          </div>
          <div class="col-auto d-flex align-items-center">
            <div v-show="isLoggedOff">
              <a
                href="login"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                data-bs-title="Log in"
              >
                <i type="button" class="ms-3 fa-solid fa-arrow-right-to-bracket fa-lg" style="color: #000;"></i>
              </a>
            </div>
            <div v-show="!isLoggedOff">
              {{ getUsername }}
              <a
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                data-bs-title="Log out"
              >
                <i type="button" class="ms-3 fa-solid fa-door-open fa-lg" style="color: #a51d2d;" @click="logOut"></i>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from 'axios'

export default {
  name: 'NavBar',
  computed: {
    isLoggedOff () {
      return this.$store.state.token === ''
    },
    getUsername () {
      return this.$store.state.username
    }
  },
  data () {
    return {
    }
  },
  methods: {
    logOut () {
      console.log('Logging out')
      this.$emit('logged-out')
      axios.defaults.headers.common.Authorization = ''

      localStorage.removeItem('token')
      localStorage.removeItem('username')

      this.$store.commit('removeToken')
      this.$store.commit('removeUsername')
    }
  }
}
</script>
