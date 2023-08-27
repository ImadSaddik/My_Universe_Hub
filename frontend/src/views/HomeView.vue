<template>
  <SearchSection />
  <GallerySection :archive="archive" @selected-item="(value) => selectedItem = value" />
  <BackToTopVue />
  <ImageDetails :item="selectedItem" />
</template>

<script>
import axios from 'axios'
import SearchSection from '@/components/SearchSection.vue'
import GallerySection from '@/components/GallerySection.vue'
import BackToTopVue from '@/components/BackToTop.vue'
import ImageDetails from '@/components/ImageDetails.vue'

export default {
  name: 'HomeView',
  components: {
    SearchSection,
    GallerySection,
    BackToTopVue,
    ImageDetails
  },
  data () {
    return {
      archive: [],
      selectedItem: ''
    }
  },
  mounted () {
    this.getArchive()
  },
  methods: {
    async getArchive () {
      await axios
        .get('/api/v1/gallery/')
        .then(response => {
          this.archive = response.data
          console.log(response.data)
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>
