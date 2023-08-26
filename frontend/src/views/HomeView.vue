<template>
  <button
      v-if="showBackToTopButton"
      class="btn btn-primary top-0 start-0"
      @click="scrollToTop"
    >
      Back to Top
  </button>
  <SearchSection />
  <GallerySection :archive="archive" />
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
