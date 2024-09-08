<template>
  <div>
    <div v-if="isLoggedIn && archive.length !== 0">
      <GallerySection :archive="archive" @selected-item="(value) => selectedItem = value" />
      <BackToTopVue />
      <ImageDetails :item="selectedItem" @unlike-image="(item) => removeItem(item)" />
    </div>
  
    <div v-if="!isLoggedIn || archive.length === 0">
      <div class="container d-flex align-items-center justify-content-center" style="height: calc(100vh - 3.5rem)">
        <div class="row">
          <h5 class="nav-link m-0">{{ getMessage() }}</h5>
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
    getEmail() {
      return this.$store.state.email;
    },
  },
  mounted () {
    this.getFavouritesArchive()
    document.title = 'Favourites'
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

      const email = this.getEmail
      await axios
        .get(`/api/v1/favourites/${email}/`)
        .then(response => {
          this.archive = response.data
        })
        .catch(error => {
        })
    },
    removeItem (item) {
      const index = this.archive.indexOf(item)
      if (index > -1) {
        this.archive.splice(index, 1)
      }
    },
    getMessage() {
      if (!this.isLoggedIn) {
        return 'Log in to see your favourites.';
      } else if (this.archive.length === 0) {
        return 'Like some images to add them to your favourites.';
      }
      return '';
    }
  }
}
</script>
