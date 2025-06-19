<template>
  <!-- Checking state -->
  <div v-if="apodStatus === 'checking'" class="overlay" role="status" aria-live="polite" aria-busy="true">
    <div class="text-center">
      <div class="spinner-border" role="status" aria-label="Loading" style="width: 3rem; height: 3rem">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Checking NASA APOD service status.</p>
    </div>
  </div>

  <!-- Down state -->
  <div v-else-if="apodStatus === 'down'" class="overlay" role="alert" aria-live="assertive">
    <div class="text-center">
      <h4 class="alert-heading"><i class="fas fa-meteor me-2" aria-hidden="true" />APOD service unavailable</h4>
      <p class="mt-3 mb-0">
        We're currently unable to connect to NASA's Astronomy Picture of the Day (APOD) service. Please try again later.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ApodStatusOverlay",
  computed: {
    apodStatus() {
      return this.$store.state.apodStatus;
    },
  },
};
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none; /* Allows clicks to pass through the overlay */
}
</style>
