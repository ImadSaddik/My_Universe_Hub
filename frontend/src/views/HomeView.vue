<template>
  <SearchSection />
  <GallerySection :archive="archive" />

  <i
    v-if="showBackToTopButton"
    type="button"
    class="fs-1 fa-solid fa-circle-arrow-up fa-2xl go-up-button"
    @click="scrollToTop"
  >
  </i>
</template>

<script>
import axios from 'axios'
import SearchSection from '@/components/SearchSection.vue'
import GallerySection from '@/components/GallerySection.vue'

export default {
  name: 'HomeView',
  components: {
    SearchSection,
    GallerySection
  },
  data () {
    return {
      archive: [],
      showBackToTopButton: false
    }
  },
  mounted () {
    this.getArchive()
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount () {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    async getArchive () {
      await axios
        .get('/api/v1/gallery/')
        .then(response => {
          this.archive = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
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
