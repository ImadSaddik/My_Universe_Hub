<template>
  <nav class="navbar navbar-expand-lg bg-white">
    <div class="container-fluid px-sm-3">
      <RouterLink
        class="navbar-brand p-0 m-0 me-5"
        data-test="nav-link-app-logo"
        to="/"
        aria-label="Go to home page"
        @click="handleNavbarItemClick(HOME_PAGE)"
      >
        <img
          data-test="app-logo"
          src="../assets/logos/galaxy_logo.svg"
          alt="MyUniverseHub galaxy logo"
          style="width: 2rem"
        />
      </RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon" />
      </button>
      <div id="navbarNavAltMarkup" class="collapse navbar-collapse">
        <div class="row w-100 m-0 navbar-nav">
          <div class="col m-0 p-0 d-lg-flex align-items-center">
            <RouterLink
              class="nav-link"
              data-test="nav-link-home"
              :class="getNavbarItemClass(HOME_PAGE)"
              to="/"
              @click="handleNavbarItemClick(HOME_PAGE)"
            >
              Home
            </RouterLink>
            <RouterLink
              class="nav-link"
              data-test="nav-link-today"
              :class="getNavbarItemClass(TODAY_PAGE)"
              to="/today"
              @click="handleNavbarItemClick(TODAY_PAGE)"
            >
              Today's picture
            </RouterLink>
            <RouterLink
              class="nav-link"
              data-test="nav-link-trending"
              :class="getNavbarItemClass(TRENDING_PAGE)"
              to="/trending"
              @click="handleNavbarItemClick(TRENDING_PAGE)"
            >
              Trending
            </RouterLink>
            <RouterLink
              class="nav-link"
              data-test="nav-link-favourites"
              :class="getNavbarItemClass(FAVOURITES_PAGE)"
              to="/favourites"
              @click="handleNavbarItemClick(FAVOURITES_PAGE)"
            >
              Favourites
            </RouterLink>
            <RouterLink
              class="nav-link"
              data-test="nav-link-contribute"
              :class="getNavbarItemClass(CONTRIBUTE_PAGE)"
              to="/contribute"
              @click="handleNavbarItemClick(CONTRIBUTE_PAGE)"
            >
              Contribute
            </RouterLink>
            <RouterLink
              class="nav-link"
              data-test="nav-link-about"
              :class="getNavbarItemClass(ABOUT_PAGE)"
              to="/about"
              @click="handleNavbarItemClick(ABOUT_PAGE)"
            >
              About
            </RouterLink>
            <hr class="d-block d-lg-none" />
          </div>
          <div class="col-auto d-flex p-0 align-items-center">
            <!-- GitHub logo and star count -->
            <a
              :href="githubRepoUrl"
              data-cy="github-link"
              target="_blank"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="GitHub repository"
              class="border-container d-flex align-items-center text-dark me-2"
            >
              <div>
                <i class="fab fa-github fa-lg" />
              </div>
              <span class="ms-2" data-test="github-star-count">{{ starCount }}</span>
            </a>

            <!-- Log in icon -->
            <a
              v-show="isLoggedOff"
              href="/login"
              data-test="nav-link-login"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="Log In"
              class="border-container"
              @click="handleNavbarItemClick(NONE)"
            >
              Log In
              <i type="button" class="ms-2 fa-solid fa-arrow-right-to-bracket fa-lg" style="color: #000" />
            </a>

            <!-- Log out icon -->
            <div
              v-show="!isLoggedOff"
              data-test="nav-link-logout"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="Log out"
              class="border-container"
              @click="logOut"
            >
              Log Out
              <i type="button" class="ms-2 fa-solid fa-door-open fa-lg" style="color: #a51d2d" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from "axios";

export default {
  name: "NavBar",
  emits: ["logged-out"],
  data() {
    return {
      HOME_PAGE: "home",
      TODAY_PAGE: "today",
      TRENDING_PAGE: "trending",
      FAVOURITES_PAGE: "favourites",
      ABOUT_PAGE: "about",
      CONTRIBUTE_PAGE: "contribute",
      NONE: "",
      starCount: 0,
      githubRepoUrl: "https://github.com/ImadSaddik/My_Universe_Hub",
    };
  },
  computed: {
    isLoggedOff() {
      return this.$store.state.token === "";
    },
    getEmail() {
      return this.$store.state.email;
    },
    getSelectedNavbarItem() {
      return this.$store.state.selectedNavbarItem;
    },
  },
  async mounted() {
    await this.fetchGitHubStars();
  },
  methods: {
    getNavbarItemClass(page) {
      return {
        active: this.getSelectedNavbarItem === page,
        "fw-bold": this.getSelectedNavbarItem === page,
      };
    },
    logOut() {
      this.$emit("logged-out");
      axios.defaults.headers.common.Authorization = "";

      localStorage.removeItem("token");
      localStorage.removeItem("email");

      this.$store.commit("removeToken");
      this.$store.commit("removeEmail");
    },
    handleNavbarItemClick(item) {
      localStorage.setItem("selectedNavbarItem", item);
      this.$store.commit("setSelectedNavbarItem", item);
    },
    async fetchGitHubStars() {
      try {
        await axios
          .get("https://api.github.com/repos/ImadSaddik/My_Universe_Hub")
          .then((response) => {
            this.starCount = response.data.stargazers_count;
          })
          .catch((error) => {});
      } catch (error) {
        console.error("Error fetching GitHub star count:", error);
      }
    },
  },
};
</script>

<style scoped>
a {
  color: black;
  text-decoration: none;
}

.navbar {
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.15);
}

.border-container {
  padding: 0.5rem 1rem 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  cursor: pointer;
}

.border-container:hover {
  background-color: #f0f0f0;
  border: 1px solid #aaa;
}
</style>
