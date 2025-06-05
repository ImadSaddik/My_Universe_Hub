<template>
  <section class="container-fluid m-0 p-0">
    <div class="row w-100 m-0 p-0 d-flex justify-content-center">
      <div class="col col-md-7 px-3 px-lg-4 outer-card-container">
        <h1 class="fs-1 fw-bold text-black mb-4">Reset password</h1>
        <div v-if="passwordChangedSuccess" class="alert alert-success alert-dismissible fade show" role="alert">
          <i class="fas fa-check-circle me-1" /> Your password has been reset successfully. You can now
          <router-link to="/login"> log in </router-link> with your new password.
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
            @click="passwordChangedSuccess = false"
          />
        </div>

        <div
          v-if="errorOccurred"
          id="reset-password-confirmation-error"
          class="alert alert-danger alert-dismissible fade show"
          role="alert"
        >
          <i class="fas fa-times-circle me-1" /> {{ errorMessage }}
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
            @click="errorOccurred = false"
          />
        </div>

        <div class="row m-0 p-0 input-group input-group-sm">
          <label for="new_password" class="mb-1 text-black p-0">New password</label>
          <div class="input-container p-0">
            <i class="fas fa-lock input-icon" aria-hidden="true" />
            <input
              id="new_password"
              v-model="new_password"
              class="input-field"
              placeholder="Your new password"
              :type="showHidePassword ? 'password' : 'text'"
              :aria-describedby="errorOccurred ? 'reset-password-confirmation-error' : null"
            />
            <i
              class="fas toggle-password-icon"
              :class="showHidePassword ? 'fa-eye' : 'fa-eye-slash'"
              :aria-label="showHidePassword ? 'Show password' : 'Hide password'"
              :aria-expanded="!showHidePassword"
              role="button"
              tabindex="0"
              @click="togglePasswordVisibility"
            />
          </div>

          <label for="re_new_password" class="mb-1 text-black p-0">Confirm new password</label>
          <div class="input-container p-0">
            <i class="fas fa-lock input-icon" aria-hidden="true" />
            <input
              id="re_new_password"
              v-model="re_new_password"
              class="input-field"
              placeholder="Confirm new password"
              :type="showHidePassword ? 'password' : 'text'"
              :aria-describedby="errorOccurred ? 'reset-password-confirmation-error' : null"
            />
            <i
              class="fas toggle-password-icon"
              :class="showHidePassword ? 'fa-eye' : 'fa-eye-slash'"
              :aria-label="showHidePassword ? 'Show password' : 'Hide password'"
              :aria-expanded="!showHidePassword"
              role="button"
              tabindex="0"
              @click="togglePasswordVisibility"
            />
          </div>

          <button class="custom-btn custom-btn-white my-3" @click="confirmResetPassword">Reset password</button>
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
      showHidePassword: true,
      errorOccurred: false,
      errorMessage: "",
    };
  },
  created() {
    document.title = "Reset password confirmation";
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
          this.errorOccurred = false;
        })
        .catch((error) => {
          this.errorOccurred = true;
          this.errorMessage = Object.values(error.response.data)[0][0];
        });
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
