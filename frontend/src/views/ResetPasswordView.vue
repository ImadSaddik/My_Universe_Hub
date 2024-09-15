<template>
  <section class="container-fluid p-2" style="height: calc(100vh - 3.5rem)">
    <div class="position-relative h-100 d-flex flex-column">
      <img
        src="../assets/reset_pass_bg.jpg"
        class="img-fluid custom-image"
        alt="..."
      />

      <div
        class="container position-absolute top-50 start-50 translate-middle align-self-center"
      >
        <div
          class="row px-2 px-sm-5 pb-5 d-flex justify-content-center align-items-center"
        >
          <div class="col col-sm-7 outer-card-container">
            <h1 class="display-5 fs-1 fw-bold text-white mb-4">
              Reset password
            </h1>

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

            <button @click="resetPassword" class="custom-btn custom-btn-white my-3">
              Submit
            </button>
            <p class="text-white text-center m-0 my-2">
              Go back to the <router-link to="/login">Log in</router-link> page. 
            </p>
          </div>
        </div>
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
.custom-image {
  height: 100%;
  object-fit: cover;
  filter: brightness(0.4);
}
</style>
