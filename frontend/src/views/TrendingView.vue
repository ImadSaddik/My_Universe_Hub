<template>
  <GallerySection :archive="getArchive" @selected-item="(value) => selectedItem = value" />
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
  computed: {
    getArchive () {
      if (this.isUserLoggedOff) {
        return this.removeLikes()
      } else {
        return this.updateArchiveLikes()
      }
    },
    isUserLoggedOff () {
      return this.$store.state.token === ''
    }
  },
  data () {
    return {
      archive: [],
      selectedItem: ''
    }
  },
  mounted () {
    this.getTrendingArchive()
    document.title = 'Trending - NASA Images'
  },
  methods: {
    async getTrendingArchive () {
      await axios
        .get('/api/v1/trending/')
        .then(response => {
          this.archive = response.data
        })
        .catch(error => {
        })
    },
    removeLikes () {
      for (let i = 0; i < this.archive.length; i++) {
        this.archive[i].image_is_liked = false
      }
      return this.archive
    },
    updateArchiveLikes () {
      const email = localStorage.getItem('email')
      for (let i = 0; i < this.archive.length; i++) {
        if (this.archive[i].liked_by_users.includes(email)) {
          this.archive[i].image_is_liked = true
        } else {
          this.archive[i].image_is_liked = false
        }
      }
      return this.archive
    }
  }
}
</script>
