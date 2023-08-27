<template>
  <div>
    <i
      v-if="showBackToTopButton"
      type="button"
      class="fs-1 fa-solid fa-circle-arrow-up fa-2xl go-up-button"
      @click="scrollToTop"
    >
    </i>
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
    bottom: 1.5em;
    right: 1em;
    cursor: pointer;
    color: #3584e4;
    z-index: 3;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }
</style>
