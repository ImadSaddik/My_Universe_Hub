<template>
  <GallerySection :archive="archive" @selected-item="(value) => selectedItem = value" />
  <BackToTopVue />
  <ImageDetails :item="selectedItem" />
</template>

<script>
import axios from 'axios'
import GallerySection from '@/components/GallerySection.vue'
import BackToTopVue from '@/components/BackToTop.vue'
import ImageDetails from '@/components/ImageDetails.vue'

export default {
  name: 'TrendingView',
  components: {
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
    this.getTrendingArchive()
  },
  methods: {
    async getTrendingArchive () {
      await axios
        .get('/api/v1/trending/')
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
