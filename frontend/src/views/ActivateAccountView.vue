<template>
  <section class="container-fluid m-0 p-0">
    <div class="row w-100 m-0 p-0 d-flex justify-content-center">
      <div class="col col-md-7 px-3 px-lg-4 outer-card-container">
        <h1 class="display-5 fs-1 fw-bold text-black mb-4">
          Activation status
        </h1>
        <div class="card-container bg-success-subtle">
          <p v-if="activationStatus" class="text-black m-0">
            <i class="fas fa-check-circle me-1"></i> Account activated successfully. You can now <router-link to="/login">log in</router-link>.
          </p>
          <p v-else-if="!activationStatus" class="text-black m-0">
            <i class="fas fa-times-circle me-1"></i> Account activation failed. Please try again.
          </p>
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
.outer-card-container {
    padding: 3rem;
}

.card-container {
  padding: 2rem;
  border-radius: 1rem;
  background-color: #ccc;
  color: black;
}

.signup-confirmation-container {
  padding: 2rem;
  border-radius: 1rem;
  color: black;
}

@media (max-width: 768px) {
    .outer-card-container {
        padding: 2rem;
    }
}
</style>
