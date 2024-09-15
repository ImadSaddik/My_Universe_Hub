<template>
  <nav class="navbar navbar-expand-lg bg-white">
    <div class="container-fluid px-sm-3">
      <a class="navbar-brand p-0 m-0 me-5" href="/" @click="handleNavbarItemClick(HOME_PAGE)">
        <img src="../assets/galaxy_logo.svg" alt="" style="width: 2rem;">
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="row w-100 m-0 navbar-nav">
          <div class="col m-0 p-0 d-lg-flex align-items-center">
            <a
              class="nav-link"
              :class="getNavbarItemClass(HOME_PAGE)"
              href="/"
              @click="handleNavbarItemClick(HOME_PAGE)"
            >
            Home
            </a>
            <a
              class="nav-link"
              :class="getNavbarItemClass(TODAY_PAGE)"
              href="/today"
              @click="handleNavbarItemClick(TODAY_PAGE)"
            >
            Today's picture
            </a>
            <a
              class="nav-link"
              :class="getNavbarItemClass(TRENDING_PAGE)"
              href="/trending"
              @click="handleNavbarItemClick(TRENDING_PAGE)"
            >
            Trending
            </a>
            <a
              class="nav-link"
              :class="getNavbarItemClass(FAVOURITES_PAGE)"
              href="/favourites"
              @click="handleNavbarItemClick(FAVOURITES_PAGE)"
            >
            Favourites
            </a>
            <hr class="d-block d-lg-none">
          </div>
          <div class="col-auto d-flex p-0 align-items-center">
            <div v-show="isLoggedOff">
              <a
                href="login"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                data-bs-title="Log in"
                @click="handleNavbarItemClick(NONE)"
              >
                <i type="button" class="ms-3 fa-solid fa-arrow-right-to-bracket fa-lg" style="color: #000;"></i>
              </a>
            </div>
            <div v-show="!isLoggedOff">
              {{ getEmail }}
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
    getEmail() {
      return this.$store.state.email;
    },
    getSelectedNavbarItem () {
      return this.$store.state.selectedNavbarItem
    }
  },
  mounted () {
    this.handleNavbarItemClick(this.HOME_PAGE)
  },
  data () {
    return {
      HOME_PAGE: 'home',
      TODAY_PAGE: 'today',
      TRENDING_PAGE: 'trending',
      FAVOURITES_PAGE: 'favourites',
      NONE: ''
    }
  },
  methods: {
    getNavbarItemClass(page) {
      return {
        active: this.getSelectedNavbarItem === page,
        'fw-bold': this.getSelectedNavbarItem === page
      };
    },
    logOut () {
      this.$emit('logged-out')
      axios.defaults.headers.common.Authorization = ''

      localStorage.removeItem('token')
      localStorage.removeItem('email')

      this.$store.commit('removeToken')
      this.$store.commit('removeEmail')
    },
    handleNavbarItemClick (item) {
      localStorage.setItem('selectedNavbarItem', item)
    }
  }
}
</script>

<style scoped>
.navbar {
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.15);
}
</style>
