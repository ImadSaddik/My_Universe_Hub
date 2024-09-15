<template>
  <section class="container-fluid p-2" style="height: calc(100vh - 3.5rem)">
    <div class="position-relative h-100 d-flex flex-column">
      <img
        src="../assets/Sign_up_bg.jpg"
        class="img-fluid custom-image"
        alt="..."
      />

      <div
        class="container position-absolute top-50 start-50 translate-middle align-self-center"
      >
        <div class="row px-4 px-sm-5 pb-5 d-flex justify-content-center">
          <div class="col col-lg-7 px-3 px-lg-4 outer-card-container">
            <h1 class="display-5 fs-1 fw-bold text-white mb-4">Sign Up</h1>
            <div
              v-if="showAlertDialog"
              class="alert alert-warning alert-dismissible fade show rounded-3"
              role="alert"
            >
              <div v-for="error in errors" :key="error">
                <strong>Error! </strong> {{ error }}
              </div>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="alert"
                aria-label="Close"
                @click="showAlertDialog = false"
              ></button>
            </div>
            <form v-if="!hideForm" @submit.prevent="submitForm">
              <label for="exampleInputUsername" class="mb-1">Username</label>
              <div class="input-container">
                <i class="fas fa-user input-icon"></i>
                <input
                  type="text"
                  class="input-field"
                  placeholder="Username"
                  id="exampleInputUsername"
                  v-model="username"
                />
              </div>
              
              <label for="exampleInputEmail" class="mb-1">Email</label>
              <div class="input-container">
                <i class="fas fa-envelope input-icon"></i>
                <input
                  class="input-field"
                  placeholder="Email"
                  id="exampleInputEmail"
                  v-model="email"
                  type="email"
                />
              </div>
              
              <label for="exampleInputPassword1" class="mb-1">Password</label>
              <div class="input-container">
                <i class="fas fa-lock input-icon"></i>
                <input
                  class="input-field"
                  placeholder="Password"
                  id="exampleInputPassword1"
                  v-model="password"
                  :type="showHidePassword ? 'password' : 'text'"
                />
                <i
                  class="fas toggle-password-icon"
                  :class="showHidePassword ? 'fa-eye' : 'fa-eye-slash'"
                  @click="togglePasswordVisibility"
                ></i>
              </div>

              <label for="exampleInputPassword2" class="mb-1">Repeat password</label>
              <div class="input-container">
                <i class="fas fa-lock input-icon"></i>
                <input
                  class="input-field"
                  placeholder="Repeat password"
                  id="exampleInputPassword2"
                  v-model="repeatPassword"
                  :type="showHidePassword ? 'password' : 'text'"
                />
                <i
                  class="fas toggle-password-icon"
                  :class="showHidePassword ? 'fa-eye' : 'fa-eye-slash'"
                  @click="togglePasswordVisibility"
                ></i>
              </div>

              <button type="submit" class="custom-btn custom-btn-white my-3">Sign Up</button>
              <p class="text-white text-center m-0 my-2">
                Already have an account? <router-link to="/login">Log in</router-link>.
              </p>
            </form>

            <div v-if="hideForm" class="signup-confirmation-container">
              <p class="m-0 p-0">
                <i class="fas fa-check-circle me-1"></i> Account created
                successfully. Please check your email to verify your account.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "SignUpView",
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
    document.title = "Sign Up";
  },
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
          this.errors = [];
          this.showAlertDialog = false;
          this.hideForm = true;
        })
        .catch((error) => {
          this.errors.push("Something went wrong. Please try again.");
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
.custom-image {
  height: 100%;
  object-fit: cover;
  filter: brightness(0.4);
}

.signup-confirmation-container {
  padding: 2rem;
  border-radius: 1rem;
  background-color: white;
  color: black;
}
</style>
