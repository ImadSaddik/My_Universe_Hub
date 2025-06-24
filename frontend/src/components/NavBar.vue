<template>
  <nav class="navbar navbar-expand-lg bg-white">
    <div class="container-fluid px-sm-3">
      <RouterLink
        class="navbar-brand p-0 m-0 me-5"
        data-testid="nav-link-app-logo"
        to="/"
        aria-label="Go to home page"
        role="button"
        tabindex="0"
        @click="handleNavbarItemClick(HOME_PAGE)"
        @keydown.enter="handleNavbarItemClick(HOME_PAGE)"
      >
        <img
          data-testid="app-logo"
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
              data-testid="nav-link-home"
              :class="getNavbarItemClass(HOME_PAGE)"
              to="/"
              @click="handleNavbarItemClick(HOME_PAGE)"
            >
              Home
            </RouterLink>
            <RouterLink
              class="nav-link"
              data-testid="nav-link-today"
              :class="getNavbarItemClass(TODAY_PAGE)"
              to="/today"
              @click="handleNavbarItemClick(TODAY_PAGE)"
            >
              Today's picture
            </RouterLink>
            <RouterLink
              class="nav-link"
              data-testid="nav-link-trending"
              :class="getNavbarItemClass(TRENDING_PAGE)"
              to="/trending"
              @click="handleNavbarItemClick(TRENDING_PAGE)"
            >
              Trending
            </RouterLink>
            <RouterLink
              class="nav-link"
              data-testid="nav-link-favourites"
              :class="getNavbarItemClass(FAVOURITES_PAGE)"
              to="/favourites"
              @click="handleNavbarItemClick(FAVOURITES_PAGE)"
            >
              Favourites
            </RouterLink>
            <RouterLink
              class="nav-link"
              data-testid="nav-link-contribute"
              :class="getNavbarItemClass(CONTRIBUTE_PAGE)"
              to="/contribute"
              @click="handleNavbarItemClick(CONTRIBUTE_PAGE)"
            >
              Contribute
            </RouterLink>
            <RouterLink
              class="nav-link"
              data-testid="nav-link-about"
              :class="getNavbarItemClass(ABOUT_PAGE)"
              to="/about"
              @click="handleNavbarItemClick(ABOUT_PAGE)"
            >
              About
            </RouterLink>
            <hr class="d-block d-lg-none" />
          </div>

          <div class="col-auto d-flex p-0">
            <!-- APOD health status indicator -->
            <a
              :href="apodUrl"
              data-testid="apod-status-indicator"
              target="_blank"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="APOD health status"
              role="status"
              aria-live="polite"
              class="border-container d-flex align-items-center text-dark me-2"
              :aria-label="getApodStatusText"
            >
              {{ getApodStatusText }}
              <i :class="getApodStatusIcon" aria-hidden="true" />
            </a>

            <!-- GitHub logo and star count -->
            <a
              :href="githubRepoUrl"
              data-testid="github-link"
              target="_blank"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="GitHub repository"
              class="border-container d-flex align-items-center text-dark me-2"
            >
              <div>
                <i class="fab fa-github fa-lg" />
              </div>
              <span class="ms-2" data-testid="github-star-count">{{ starCount }}</span>
            </a>

            <!-- Log in icon -->
            <RouterLink
              v-show="isLoggedOff"
              to="/login"
              data-testid="nav-link-login"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="Log In"
              class="border-container"
              role="button"
              tabindex="0"
              @click="handleNavbarItemClick(NONE)"
              @keydown.enter="handleNavbarItemClick(NONE)"
            >
              Log In
              <i type="button" class="ms-2 fa-solid fa-arrow-right-to-bracket fa-lg" style="color: #000" />
            </RouterLink>

            <!-- Log out icon -->
            <div
              v-show="!isLoggedOff"
              data-testid="nav-link-logout"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="Log out"
              class="border-container"
              role="button"
              tabindex="0"
              @click="logOut"
              @keydown.enter="logOut"
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
      apodUrl: "https://apod.nasa.gov/apod/archivepix.html",
    };
  },
  computed: {
    apodStatus() {
      return this.$store.state.apodStatus;
    },
    isLoggedOff() {
      return this.$store.state.token === "";
    },
    getEmail() {
      return this.$store.state.email;
    },
    getSelectedNavbarItem() {
      return this.$store.state.selectedNavbarItem;
    },
    getApodStatusIcon() {
      if (this.apodStatus === "checking") {
        return "ms-2 fa-solid fa-hurricane fa-spin";
      }
      if (this.apodStatus === "up") {
        return "ms-2 fa-solid fa-circle text-success";
      }
      if (this.apodStatus === "down") {
        return "ms-2 fa-solid fa-circle apod-down";
      }
      return "";
    },
    getApodStatusText() {
      if (this.apodStatus === "checking") {
        return "Checking";
      }
      if (this.apodStatus === "up") {
        return "APOD is up";
      }
      if (this.apodStatus === "down") {
        return "APOD is down";
      }
      return "";
    },
  },
  async mounted() {
    await this.fetchGitHubStars();
    await this.checkApodHealth();
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
    async checkApodHealth() {
      this.$store.commit("setApodStatus", "checking");
      try {
        const response = await axios.get("/api/v1/apod-health/");
        this.$store.commit("setApodStatus", response.data.status);
      } catch (error) {
        console.error("Error checking APOD health:", error);
        this.$store.commit("setApodStatus", "down");
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

.apod-down {
  color: #98242f;
}
</style>
