<template>
  <section class="container-fluid m-0 p-0">
    <div class="row w-100 m-0 p-0 d-flex justify-content-center">
      <div class="col col-md-7 px-3 px-lg-4 outer-card-container">
        <h1 class="fs-1 fw-bold text-black mb-4">Reset password</h1>
        <div
          v-if="resetLinkSent"
          class="alert alert-success alert-dismissible fade show"
          role="alert"
        >
          Check your email for a link to reset your password.
          <button
            @click="resetLinkSent = false"
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
          ></button>
        </div>

        <div
          v-if="errorOccurred"
          class="alert alert-danger alert-dismissible fade show"
          role="alert"
        >
          {{ errorMessage }}
          <button
            @click="errorOccurred = false"
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
          ></button>
        </div>

        <label for="exampleInputEmail" class="mb-1 text-black">Email</label>
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

        <button @click="resetPassword" class="custom-btn custom-btn-white my-3">
          Submit
        </button>
        <p class="text-black text-center m-0 my-2">
          Go back to the <router-link to="/login">Log in</router-link> page. 
        </p>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "ResetPasswordView",
  components: {},
  mounted() {
    document.title = "Reset Password";
  },
  data() {
    return {
      email: "",
      resetLinkSent: false,
      errorOccurred: false,
      errorMessage: "",
    };
  },
  methods: {
    async resetPassword() {
      if (this.errorExist()) {
        return;
      }

      const data = JSON.stringify({
        email: this.email,
      });

      await axios
        .post("/api/v1/users/reset_password/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          this.resetLinkSent = true;
          this.errorOccurred = false;
        })
        .catch((error) => {
          this.errorMessage = error.response.data.email[0];
          this.errorOccurred = true;
        });
    },
    errorExist() {
      if (this.email === "") {
        this.errorOccurred = true;
        this.errorMessage = "Email is required.";
        return true;
      }
      return false;
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
