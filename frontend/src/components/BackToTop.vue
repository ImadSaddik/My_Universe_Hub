<template>
  <div>
    <img
      v-show="showBackToTopButton"
      data-testid="scroll-to-top-button"
      src="../assets/circle-arrow-up-solid.svg"
      type="button"
      class="img go-up-button"
      alt="Scroll to top button"
      role="button"
      tabindex="0"
      @click="scrollToTop"
      @keydown.enter="scrollToTop"
    />
  </div>
</template>

<script>
export default {
  name: "BackToTop",
  components: {},
  data() {
    return {
      showBackToTopButton: false,
    };
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    },
    handleScroll() {
      this.showBackToTopButton = window.scrollY > 500;
    },
  },
};
</script>

<style scoped>
.go-up-button {
  position: fixed;
  width: 3rem;
  bottom: 1.5rem;
  right: 1.5rem;
  cursor: pointer;
  z-index: 3;
}

.go-up-button:hover {
  opacity: 0.8;
}
</style>
