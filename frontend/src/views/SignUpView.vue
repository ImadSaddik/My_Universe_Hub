<template>
  <section class="container-fluid m-0 p-0">
    <div class="row w-100 m-0 p-0 d-flex justify-content-center">
      <div class="col col-md-7 px-3 px-lg-4 outer-card-container">
        <h1 class="fs-1 fw-bold text-black mb-4">Sign Up</h1>
        <div
          v-if="showAlertDialog"
          id="signup-error"
          class="alert alert-danger alert-dismissible fade show rounded-3"
          role="alert"
        >
          <div v-for="error in errors" :key="error"><i class="fas fa-times-circle me-1" /> {{ error }}</div>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
            @click="showAlertDialog = false"
          />
        </div>
        <form v-if="!hideForm" @submit.prevent="submitForm">
          <label for="exampleInputUsername" class="mb-1 text-black">Username</label>
          <div class="input-container">
            <i class="fas fa-user input-icon" />
            <input
              id="exampleInputUsername"
              v-model="username"
              type="text"
              class="input-field"
              placeholder="John Doe"
              :aria-describedby="showAlertDialog ? 'signup-error' : null"
            />
          </div>

          <label for="exampleInputEmail" class="mb-1 text-black">Email</label>
          <div class="input-container">
            <i class="fas fa-envelope input-icon" />
            <input
              id="exampleInputEmail"
              v-model="email"
              class="input-field"
              placeholder="your.email@example.com"
              type="email"
              :aria-describedby="showAlertDialog ? 'signup-error' : null"
            />
          </div>

          <label for="exampleInputPassword1" class="mb-1 text-black">Password</label>
          <div class="input-container">
            <i class="fas fa-lock input-icon" />
            <input
              id="exampleInputPassword1"
              v-model="password"
              class="input-field"
              placeholder="Password"
              :type="showHidePassword ? 'password' : 'text'"
              :aria-describedby="showAlertDialog ? 'signup-error' : null"
            />
            <i
              class="fas toggle-password-icon"
              :class="showHidePassword ? 'fa-eye' : 'fa-eye-slash'"
              @click="togglePasswordVisibility"
            />
          </div>

          <label for="exampleInputPassword2" class="mb-1 text-black">Repeat password</label>
          <div class="input-container">
            <i class="fas fa-lock input-icon" />
            <input
              id="exampleInputPassword2"
              v-model="repeatPassword"
              class="input-field"
              placeholder="Repeat password"
              :type="showHidePassword ? 'password' : 'text'"
              :aria-describedby="showAlertDialog ? 'signup-error' : null"
            />
            <i
              class="fas toggle-password-icon"
              :class="showHidePassword ? 'fa-eye' : 'fa-eye-slash'"
              @click="togglePasswordVisibility"
            />
          </div>

          <button type="submit" class="custom-btn custom-btn-white my-3">Sign Up</button>
          <p class="text-black text-center m-0 my-2">
            Already have an account? <router-link to="/login"> Log in </router-link>.
          </p>
        </form>

        <div v-if="hideForm" class="signup-confirmation-container">
          <p class="m-0 p-0">
            <i class="fas fa-check-circle me-1" /> Account created successfully. Please check your email to verify your
            account.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "SignUpView",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      repeatPassword: "",
      showHidePassword: true,
      showAlertDialog: false,
      hideForm: false,
      errors: [],
    };
  },
  computed: {
    isLoggedOff() {
      return this.$store.state.token === "";
    },
  },
  created() {
    document.title = "Sign Up";
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
        return;
      }

      const formData = {
        name: this.username,
        email: this.email,
        password: this.password,
        re_password: this.repeatPassword,
      };

      axios.defaults.headers.common.Authorization = "";
      await axios
        .post("/api/v1/users/", formData)
        .then((response) => {
          this.showAlertDialog = false;
          this.hideForm = true;
          this.errors = [];
        })
        .catch((error) => {
          const errorData = error.response.data;
          for (const key in errorData) {
            this.errors = errorData[key];
          }
          this.showAlertDialog = true;
        });
    },
    errorExist() {
      this.errors = [];

      if (this.username === "") {
        this.errors.push("The username field is required.");
      }

      if (this.email === "") {
        this.errors.push("The email fiels is required.");
      }

      if (this.password === "") {
        this.errors.push("The password field is required.");
      }

      if (this.repeatPassword === "") {
        this.errors.push("The repeat password field is required.");
      }

      if (this.password !== this.repeatPassword) {
        this.errors.push("The two password fields didn't match.");
      }

      if (this.errors.length) {
        this.showAlertDialog = true;
        return true;
      }
    },
  },
};
</script>

<style scoped>
.outer-card-container {
  padding: 3rem;
}

.signup-confirmation-container {
  padding: 2rem;
  border-radius: 1rem;
  background-color: white;
  color: black;
}

@media (max-width: 768px) {
  .outer-card-container {
    padding: 2rem;
  }
}
</style>
