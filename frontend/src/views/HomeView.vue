<template>
  <SearchSection @search="(query) => search(query)" />
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
  created () {
    this.$store.commit('setSelectedNavbarItem', 'home')
  },
  mounted () {
    this.getArchive()
    document.title = 'NASA Images'
  },
  methods: {
    async getArchive () {
      axios.defaults.headers.common.Authorization = ''
      await axios
        .get('/api/v1/gallery/')
        .then(response => {
          const username = localStorage.getItem('username')
          this.archive = response.data

          for (let i = 0; i < this.archive.length; i++) {
            if (this.archive[i].liked_by_users.includes(username)) {
              this.archive[i].image_is_liked = true
            } else {
              this.archive[i].image_is_liked = false
            }
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    async search (query) {
      if (query.trim().length === 0) {
        this.getArchive()
      } else {
        await axios
          .get(`/api/v1/search/${query}/`)
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
}
</script>
