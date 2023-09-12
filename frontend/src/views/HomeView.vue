<template>
  <SearchSection @search="(query) => search(query)" />
  <GallerySection :archive="getUpdatedArchive" @selected-item="(value) => selectedItem = value" />
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
  computed: {
    getUpdatedArchive () {
      if (this.isUserLoggedOff) {
        console.log('User is logged off')
        return this.removeLikes()
      } else {
        console.log('User is logged in')
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
          this.archive = response.data
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
    },
    removeLikes () {
      for (let i = 0; i < this.archive.length; i++) {
        this.archive[i].image_is_liked = false
      }
      return this.archive
    },
    updateArchiveLikes () {
      const username = localStorage.getItem('username')

      for (let i = 0; i < this.archive.length; i++) {
        if (this.archive[i].liked_by_users.includes(username)) {
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
