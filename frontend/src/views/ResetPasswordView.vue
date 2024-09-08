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
        <div
          class="row px-2 px-sm-5 pb-5 d-flex justify-content-center align-items-center"
        >
          <div class="p-0 col col-sm-6">
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

            <div class="row m-0 p-0 input-group input-group-sm">
              <label for="email" class="mb-2 p-0 fw-bold text-white"
                >Email Address</label
              >
              <input
                id="email"
                type="email"
                class="form-control rounded-3 py-2 px-3 mb-4"
                placeholder="Your email"
                v-model="email"
              />
            </div>
            <p class="text-white">
              Or <a href="/login">Click here</a>, to go back to the log in page.
            </p>
            <button @click="resetPassword" class="btn btn-primary">
              Submit
            </button>
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
          this.errorMessage = error.response.data.detail;
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
