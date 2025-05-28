<template>
  <div>
    <div class="background-image" />
    <div v-if="isLoggedIn && archive.length !== 0" class="mt-3">
      <GallerySection
        :archive="archive"
        :should-show-load-more-button="shouldShowLoadMoreButton"
        @selected-item="(value) => (selectedItem = value)"
        @increase-limit="increaseLimit()"
        @unlike-image="(item) => removeItem(item)"
      />
      <BackToTopVue />
      <ImageDetails :item="selectedItem" @unlike-image="(item) => removeItem(item)" />
    </div>

    <div v-if="!isLoggedIn || archive.length === 0">
      <div class="container d-flex align-items-center justify-content-center" style="height: calc(100vh - 3.5rem)">
        <div class="row">
          <h5 class="nav-link m-0">
            {{ getMessage() }}
          </h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import GallerySection from "@/components/GallerySection.vue";
import BackToTopVue from "@/components/BackToTop.vue";
import ImageDetails from "@/components/ImageDetails.vue";

export default {
  name: "FavouritesView",
  components: {
    GallerySection,
    BackToTopVue,
    ImageDetails,
  },
  data() {
    return {
      archive: [],
      archiveFullSize: null,
      selectedItem: "",
      incrementSize: 10,
    };
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.token !== "";
    },
    getEmail() {
      return this.$store.state.email;
    },
    shouldShowLoadMoreButton() {
      return this.archive.length < this.archiveFullSize;
    },
  },
  created() {
    document.title = "Favourites";
  },
  async mounted() {
    await this.getFavouritesArchive();
    await this.getFavouritesArchiveSize();
  },
  methods: {
    async increaseLimit() {
      await this.getFavouritesArchive();
    },
    async getFavouritesArchive() {
      if (!this.isLoggedIn) {
        return;
      }

      const email = this.getEmail;
      const start_index = this.archive.length;
      const end_index = start_index + this.incrementSize;
      await axios
        .get(`/api/v1/favourites/${email}/${start_index}/${end_index}/`)
        .then((response) => {
          this.archive.push(...response.data);
        })
        .catch((error) => {});
    },
    async getFavouritesArchiveSize() {
      if (!this.isLoggedIn) {
        return;
      }

      const email = this.getEmail;
      await axios
        .get(`/api/v1/favourites/${email}/count/`)
        .then((response) => {
          this.archiveFullSize = response.data.count;
        })
        .catch((error) => {});
    },
    removeItem(item) {
      const index = this.archive.indexOf(item);
      if (index > -1) {
        this.archive.splice(index, 1);
      }
      this.archiveFullSize -= 1;
    },
    getMessage() {
      if (!this.isLoggedIn) {
        return "Log in to see your favourites.";
      } else if (this.archive.length === 0) {
        return "Like some images to add them to your favourites.";
      }
      return "";
    },
  },
};
</script>

<style scoped>
.background-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  scale: 2;
  background: url("../assets/logos/galaxy_logo.svg") no-repeat center center;
  opacity: 0.02;
  z-index: -1;
}
</style>
