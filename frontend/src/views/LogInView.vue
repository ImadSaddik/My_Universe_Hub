<template>
  <section class="container-fluid p-2" style="height: calc(100vh - 3.5rem)">
    <div class="position-relative h-100 d-flex flex-column">
      <img
        src="../assets/Log_in_bg.jpg"
        class="img-fluid custom-image"
        alt="..."
      />

      <div
        class="container position-absolute top-50 start-50 translate-middle align-self-center"
      >
        <div class="row px-4 px-sm-5 pb-5 d-flex justify-content-center">
          <div class="col col-lg-7 px-3 px-lg-4 outer-card-container">
            <h1 class="display-5 fs-1 fw-bold text-white mb-4">Log In</h1>
            <div
              v-if="showAlertDialog"
              class="alert alert-warning alert-dismissible fade show rounded-3"
              role="alert"
            >
              <strong>Error! </strong> {{ errorMessage }}
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="alert"
                aria-label="Close"
                @click="showAlertDialog = false"
              ></button>
            </div>
            <form @submit.prevent="submitForm">
              <label for="email" class="mb-1">Email</label>
              <div class="input-container">
                <i class="fas fa-envelope input-icon"></i>
                <input
                  class="input-field"
                  placeholder="Email"
                  id="email"
                  v-model="email"
                  type="email"
                  name="email"
                  autocomplete="username"
                />
              </div>

              <label for="current-password" class="mb-1">Password</label>
              <div class="input-container">
                <i class="fas fa-lock input-icon"></i>
                <input
                  class="input-field"
                  placeholder="Password"
                  id="current-password"
                  v-model="password"
                  :type="showHidePassword ? 'password' : 'text'"
                  name="password"
                  autocomplete="current-password"
                />
                <i
                  class="fas toggle-password-icon"
                  :class="showHidePassword ? 'fa-eye' : 'fa-eye-slash'"
                  @click="togglePasswordVisibility"
                ></i>
              </div>

              <button type="submit" class="custom-btn custom-btn-white my-3">Log In</button>
              <p class="text-white text-center m-0 my-2">
                Forgot password? <router-link to="/reset_password">Click here</router-link>
              </p>
              <p class="text-white text-center m-0">
                Don't have an account? <router-link to="/signup">Sign up</router-link>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "LogInView",
  computed: {
    isLoggedOff() {
      return this.$store.state.token === "";
    },
  },
  created() {
    if (!this.isLoggedOff) {
      this.$router.push({ name: "home", replace: true });
    }
  },
  mounted() {
    document.title = "Log In";
  },
  data() {
    return {
      email: "",
      password: "",
      showHidePassword: true,
      showAlertDialog: false,
      errorMessage: "",
    };
  },
  methods: {
    togglePasswordVisibility() {
      this.showHidePassword = !this.showHidePassword;
    },
    async submitForm() {
      if (this.errorExist()) {
        this.showAlertDialog = true;
        return;
      }

      axios.defaults.headers.common.Authorization = "";
      localStorage.removeItem("token");

      const formData = {
        email: this.email,
        password: this.password,
      };

      await axios
        .post("/api/v1/jwt/create", formData)
        .then((response) => {
          const token = response.data.access;
          axios.defaults.headers.common.Authorization = "Token " + token;

          localStorage.setItem("token", token);
          this.$store.dispatch("login", token);

          localStorage.setItem("email", this.email);
          this.$store.commit("setEmail", this.email);

          localStorage.setItem("selectedNavbarItem", "home");
          this.$store.commit("setSelectedNavbarItem", "home");

          this.$router.push({ name: "home", replace: true });
        })
        .catch((error) => {
          this.showAlertDialog = true;
          this.errorMessage = error.response.data.detail;
        });
    },
    errorExist() {
      let isEmailValid = this.email !== "";
      let isPasswordValid = this.password !== "";

      if (!isEmailValid || !isPasswordValid) {
        this.errorMessage = "Please fill in all the fields.";
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>

<style scoped>
.custom-image {
  height: 100%;
  object-fit: cover;
  filter: brightness(0.4);
}
</style>
