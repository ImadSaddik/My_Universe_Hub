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
              v-if="passwordChangedSuccess"
              class="alert alert-success alert-dismissible fade show"
              role="alert"
            >
              Your password has been reset successfully. You can now
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
              {{ errorMessage }}
              <button
                @click="errorOccurred = false"
                type="button"
                class="btn-close"
                data-bs-dismiss="alert"
                aria-label="Close"
              ></button>
            </div>

            <div class="row input-group input-group-sm">
              <div class="col">
                <label for="new_password" class="mb-2 fw-bold text-white"
                  >New password</label
                >
                <input
                  id="new_password"
                  type="password"
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="Your new password"
                  v-model="new_password"
                />

                <label for="re_new_password" class="mt-3 mb-2 fw-bold text-white"
                  >Confirm new password</label
                >
                <input
                  id="re_new_password"
                  type="password"
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="Confirm new password"
                  v-model="re_new_password"
                />

                <button
                  @click="confirmResetPassword"
                  class="btn btn-primary mt-4"
                >
                  Reset password
                </button>
              </div>
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
  filter: brightness(0.4);
}
</style>
