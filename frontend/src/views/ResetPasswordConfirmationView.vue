<template>
  <section class="container-fluid p-2" style="height: calc(100vh - 3.5rem)">
    <div class="position-relative h-100 d-flex flex-column">
      <img
        src="../assets/reset_pass_confirm_bg.jpg"
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
            <h1 class="display-5 fs-1 fw-bold text-white m-0 p-0 mb-4">
              Reset password
            </h1>

            <div
              v-if="passwordChangedSuccess"
              class="alert alert-success alert-dismissible fade show"
              role="alert"
            >
              <i class="fas fa-check-circle me-1"></i> Your password has been reset successfully. You can now
              <router-link to="/login">log in</router-link> with your new
              password.
              <button
                @click="passwordChangedSuccess = false"
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
              <i class="fas fa-times-circle me-1"></i> {{ errorMessage }}
              <button
                @click="errorOccurred = false"
                type="button"
                class="btn-close"
                data-bs-dismiss="alert"
                aria-label="Close"
              ></button>
            </div>

            <div class="row m-0 p-0 input-group input-group-sm">
              <label for="new_password" class="mb-1 p-0">New password</label>
              <div class="input-container p-0">
                <i class="fas fa-lock input-icon"></i>
                <input
                  class="input-field"
                  placeholder="Your new password"
                  id="new_password"
                  v-model="new_password"
                  :type="showHidePassword ? 'password' : 'text'"
                />
                <i
                  class="fas toggle-password-icon"
                  :class="showHidePassword ? 'fa-eye' : 'fa-eye-slash'"
                  @click="togglePasswordVisibility"
                ></i>
              </div>

              <label for="re_new_password" class="mb-1 p-0">Confirm new password</label>
              <div class="input-container p-0">
                <i class="fas fa-lock input-icon"></i>
                <input
                  class="input-field"
                  placeholder="Confirm new password"
                  id="re_new_password"
                  v-model="re_new_password"
                  :type="showHidePassword ? 'password' : 'text'"
                />
                <i
                  class="fas toggle-password-icon"
                  :class="showHidePassword ? 'fa-eye' : 'fa-eye-slash'"
                  @click="togglePasswordVisibility"
                ></i>
              </div>
              
              <button
                @click="confirmResetPassword"
                class="custom-btn custom-btn-white my-3"
              >
                Reset password
              </button>
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
  name: "ResetPassword",
  data() {
    return {
      new_password: "",
      re_new_password: "",
      passwordChangedSuccess: false,
      errorOccurred: false,
      errorMessage: "",
    };
  },
  methods: {
    togglePasswordVisibility() {
      this.showHidePassword = !this.showHidePassword;
    },
    async confirmResetPassword() {
      const data = JSON.stringify({
        uid: this.$route.params.uid,
        token: this.$route.params.token,
        new_password: this.new_password,
        re_new_password: this.re_new_password,
      });

      await axios
        .post("/api/v1/users/reset_password_confirm/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          this.passwordChangedSuccess = true;
        })
        .catch((error) => {
          this.errorOccurred = true;
          this.errorMessage = Object.values(error.response.data)[0][0];
        });
    },
  },
  mounted() {
    document.title = "Reset password confirmation";
  },
};
</script>

<style scoped>
.custom-image {
  height: 100%;
  object-fit: cover;
  filter: brightness(0.8);
}
</style>
