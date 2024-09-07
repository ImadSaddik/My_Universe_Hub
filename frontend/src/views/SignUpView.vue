<template>
  <section class="container-fluid" style="height: calc(100vh - 70px)">
    <div class="position-relative h-100 d-flex flex-column">
      <img
        src="../assets/Sign_up_bg.jpg"
        class="img-fluid custom-image"
        alt="..."
      />

      <div
        class="container position-absolute top-50 start-50 translate-middle align-self-center"
      >
        <div class="row px-2 px-sm-5 pb-5 d-flex justify-content-center">
          <div class="col col-sm-6">
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
              <div class="input-group input-group-sm mb-3">
                <input
                  type="text"
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="Username"
                  id="exampleInputUsername"
                  v-model="username"
                />
              </div>
              <div class="input-group input-group-sm mb-3">
                <input
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="Email"
                  id="exampleInputEmail"
                  v-model="email"
                  type="email"
                />
              </div>
              <div class="input-group input-group-sm mb-3">
                <input
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="Password"
                  id="exampleInputPassword1"
                  v-model="password"
                  :type="showHidePassword ? 'password' : 'text'"
                />
              </div>
              <div class="input-group input-group-sm mb-3">
                <input
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="Repeat password"
                  id="exampleInputPassword2"
                  v-model="repeatPassword"
                  :type="showHidePassword ? 'password' : 'text'"
                />
              </div>
              <div class="mb-3 form-check">
                <label
                  class="form-check-label text-white"
                  for="showHidePasswordCheckBox"
                  >{{
                    showHidePassword ? "Show password" : "Hide password"
                  }}</label
                >
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="showHidePasswordCheckBox"
                  @click="showHidePassword = !showHidePassword"
                />
              </div>
              <p class="text-white">
                Or <a href="/login">Click here</a>, if you already have an
                account.
              </p>
              <button type="submit" class="btn btn-primary">Submit</button>
            </form>

            <div v-if="hideForm" class="signup-confirmation-container">
              <p class="m-0 p-0">
                Account created successfully. Please check your email to verify
                your account.
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
          console.log("successfully signed up");
        })
        .catch((error) => {
          console.log(error);
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
