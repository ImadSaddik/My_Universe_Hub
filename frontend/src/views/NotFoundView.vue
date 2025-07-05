<template>
  <section class="container">
    <h1 class="custom-title-text">404 - Page not found</h1>
    <p class="custom-small-text">Sorry, the page you are looking for does not exist.</p>
    <img
      class="stars-and-galaxies-image"
      src="../assets/logos/stars_and_galaxies.svg"
      alt="MyUniverseHub galaxy logo"
    />
  </section>
  <img class="telescope-image" src="../assets/logos/telescope.svg" alt="Telescope logo" />
</template>

<script>
export default {
  name: "NotFoundView",
  created() {
    document.title = "Page not found";
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
</style>
