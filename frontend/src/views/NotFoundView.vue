<template>
  <section class="container" aria-labelledby="error-heading">
    <h1 id="error-heading" class="custom-title-text">404 - Page not found</h1>
    <p class="custom-small-text">
      Sorry, the page you are looking for does not exist.
      <router-link to="/">Return to Home</router-link>
    </p>
    <img
      class="stars-and-galaxies-image"
      src="../assets/logos/stars_and_galaxies.svg"
      alt="Decorative image of stars and galaxies representing the MyUniverseHub theme"
    />
  </section>
  <img
    class="telescope-image"
    src="../assets/logos/telescope.svg"
    alt="Telescope image"
    aria-hidden="true"
    role="presentation"
  />
</template>

<script>
export default {
  name: "NotFoundView",
  created() {
    document.title = "404 - Page not found | MyUniverseHub";
    localStorage.setItem("selectedNavbarItem", "");
    this.$store.commit("setSelectedNavbarItem", "");
  },
};
</script>

<style scoped>
.container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.stars-and-galaxies-image {
  width: 600px;
  height: auto;
  margin-top: 20px;
}

.telescope-image {
  position: fixed;
  bottom: 0;
  left: 10%;
  width: 200px;
  height: auto;
}

@media (max-width: 768px) {
  .stars-and-galaxies-image {
    width: 70%;
    height: auto;
  }

  .telescope-image {
    display: none;
  }
}
</style>
