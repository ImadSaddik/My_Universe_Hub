<template>
  <div v-if="isLoggedIn">
    <GallerySection :archive="archive" @selected-item="(value) => selectedItem = value" />
    <BackToTopVue />
    <ImageDetails :item="selectedItem" @unlike-image="(item) => removeItem(item)" />
  </div>

  <div v-else>
    <div class="container d-flex align-items-center justify-content-center" style="height: 90vh;">
      <div class="row">
        <div class="col">
          <h5 class="nav-link">Log in to see your favourites</h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import GallerySection from '@/components/GallerySection.vue'
import BackToTopVue from '@/components/BackToTop.vue'
import ImageDetails from '@/components/ImageDetails.vue'

export default {
  name: 'FavouritesView',
  components: {
    GallerySection,
    BackToTopVue,
    ImageDetails
  },
  computed: {
    isLoggedIn () {
      return this.$store.state.token !== ''
    },
    getUsername () {
      return this.$store.state.username
    }
  },
  mounted () {
    this.getFavouritesArchive()
  },
  data () {
    return {
      archive: [],
      selectedItem: ''
    }
  },
  methods: {
    async getFavouritesArchive () {
      if (!this.isLoggedIn) {
        return
      }

      const username = this.getUsername
      await axios
        .get(`/api/v1/favourites/${username}/`)
        .then(response => {
          console.log(response)
          this.archive = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    removeItem (item) {
      const index = this.archive.indexOf(item)
      if (index > -1) {
        this.archive.splice(index, 1)
      }
    }
  }
}
</script>
