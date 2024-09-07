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
              Activation status
            </h1>
            <p v-if="activationStatus" class="text-white">
              Account activated successfully. You can now <router-link to="/login">log in</router-link>.
            </p>
            <p v-else-if="activationStatus === false" class="text-white">
              Account activation failed. Please try again.
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
  name: "ActivateAccountView",
  data() {
    return {
      activationStatus: null,
    };
  },
  methods: {
    async activateAccount() {
      const data = JSON.stringify({
        uid: this.$route.params.uid,
        token: this.$route.params.token,
      });

      await axios
        .post("/api/v1/users/activation/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          this.activationStatus = true;
        })
        .catch((error) => {
          this.activationStatus = false;
          console.error(error);
        });
    },
  },
  created() {
    this.activateAccount();
  },
  mounted() {
    document.title = "Activate account";
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
