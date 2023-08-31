<template>
  <div >
    <img
      v-if="showBackToTopButton"
      src="../assets/circle-arrow-up-solid.svg"
      type="button"
      class="img go-up-button"
      @click="scrollToTop"
    >
  </div>
</template>

<script>
export default {
  name: 'BackToTop',
  components: {
  },
  data () {
    return {
      showBackToTopButton: false
    }
  },
  mounted () {
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount () {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    scrollToTop () {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    },
    handleScroll () {
      this.showBackToTopButton = window.scrollY > 500
    }
  }
}
</script>

<style scoped>
  .go-up-button {
    position: fixed;
    width: 40px;
    bottom: 1.75em;
    right: 1.5em;
    cursor: pointer;
    z-index: 3;
  }
</style>
