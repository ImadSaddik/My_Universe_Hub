<template>
  <section class="container-fluid m-0 p-0">
    <div class="row w-100 m-0 p-0 d-flex justify-content-center">
      <div class="col col-md-7 px-3 px-lg-4 outer-card-container">
        <h1 class="fs-1 fw-bold text-black mb-4">Log In</h1>
        <div v-if="showAlertDialog" class="alert alert-danger alert-dismissible fade show rounded-3" role="alert">
          <i class="fas fa-times-circle me-1" /> {{ errorMessage }}
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
            @click="showAlertDialog = false"
          />
        </div>
        <form @submit.prevent="submitForm">
          <label for="email" class="mb-1 text-black">Email</label>
          <div class="input-container">
            <i class="fas fa-envelope input-icon" />
            <input
              id="email"
              v-model="email"
              class="input-field"
              placeholder="Email"
              type="email"
              name="email"
              autocomplete="username"
            />
          </div>

          <label for="current-password" class="mb-1 text-black">Password</label>
          <div class="input-container">
            <i class="fas fa-lock input-icon" />
            <input
              id="current-password"
              v-model="password"
              class="input-field"
              placeholder="Password"
              :type="showHidePassword ? 'password' : 'text'"
              name="password"
              autocomplete="current-password"
            />
            <i
              class="fas toggle-password-icon"
              :class="showHidePassword ? 'fa-eye' : 'fa-eye-slash'"
              @click="togglePasswordVisibility"
            />
          </div>

          <button type="submit" class="custom-btn custom-btn-white my-3">Log In</button>
          <p class="text-black text-center m-0 my-2">
            Forgot password?
            <router-link to="/reset_password"> Click here </router-link>
          </p>
          <p class="text-black text-center m-0">
            Don't have an account?
            <router-link to="/signup"> Sign up </router-link>
          </p>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "LogInView",
  data() {
    return {
      email: "",
      password: "",
      showHidePassword: true,
      showAlertDialog: false,
      errorMessage: "",
    };
  },
  computed: {
    isLoggedOff() {
      return this.$store.state.token === "";
    },
  },
  created() {
    document.title = "Log In";
    if (!this.isLoggedOff) {
      this.$router.push({ name: "home", replace: true });
    }
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
.outer-card-container {
  padding: 3rem;
}

@media (max-width: 768px) {
  .outer-card-container {
    padding: 2rem;
  }
}
</style>
