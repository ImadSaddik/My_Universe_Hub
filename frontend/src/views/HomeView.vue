<template>
  <ApodStatusOverlay />

  <!-- Up state -->
  <div v-if="apodStatus === 'up'">
    <SearchSection @search="(query) => search(query)" />
    <GallerySection
      :archive="getUpdatedArchive"
      :should-show-load-more-button="shouldShowLoadMoreButton"
      :search-result-count="searchArchiveSize"
      @selected-item="(value) => (selectedItem = value)"
      @increase-limit="increaseLimit()"
    />
    <BackToTopVue />
    <ImageDetails :item="selectedItem" />
  </div>
</template>

<script>
import axios from "axios";
import SearchSection from "@/components/SearchSection.vue";
import GallerySection from "@/components/GallerySection.vue";
import BackToTopVue from "@/components/BackToTop.vue";
import ImageDetails from "@/components/ImageDetails.vue";
import ApodStatusOverlay from "@/components/ApodStatusOverlay.vue";

export default {
  name: "HomeView",
  components: {
    SearchSection,
    GallerySection,
    BackToTopVue,
    ImageDetails,
    ApodStatusOverlay,
  },
  data() {
    return {
      archive: [],
      archiveSize: null,
      searchArchive: [],
      searchArchiveSize: null,
      selectedItem: "",
      incrementSize: 10,
      query: "",
      isSearchResultEmpty: false,
    };
  },
  computed: {
    apodStatus() {
      return this.$store.state.apodStatus;
    },
    getUpdatedArchive() {
      const archive = this.query.trim().length === 0 ? this.archive : this.searchArchive;

      if (this.isUserLoggedOff) {
        return this.removeLikes(archive);
      } else {
        return this.updateArchiveLikes(archive);
      }
    },
    isUserLoggedOff() {
      return this.$store.state.token === "";
    },
    shouldShowLoadMoreButton() {
      if (this.query.trim().length === 0) {
        return this.archive.length < this.archiveSize;
      } else {
        return this.searchArchive.length < this.searchArchiveSize;
      }
    },
  },
  watch: {
    apodStatus(newStatus, oldStatus) {
      if (newStatus === "up" && oldStatus !== "up") {
        this.getArchive();
        this.getArchiveSize();
      }
    },
  },
  created() {
    document.title = "Home";
    this.$store.commit("setSelectedNavbarItem", "home");
  },
  async mounted() {
    if (this.apodStatus === "up") {
      await this.getArchive();
      await this.getArchiveSize();
    }
    await logUserVisit();
  },
  methods: {
    async search(query) {
      this.query = query;
      this.archive = [];
      this.searchArchive = [];

      if (this.query.trim().length === 0) {
        // This means, I am not searching. Retrieve the full archive.
        await this.getArchive();
      } else {
        // This means, I am searching. Retrieve the search archive.
        await this.getSearchArchive();
      }
    },
    async increaseLimit() {
      if (this.query.trim().length === 0) {
        await this.getArchive();
      } else {
        await this.getSearchArchive();
      }
    },
    async getArchive() {
      axios.defaults.headers.common.Authorization = "";
      const start_index = this.archive.length;
      const end_index = start_index + this.incrementSize;
      await axios
        .get(`/api/v1/gallery/${start_index}/${end_index}/`)
        .then((response) => {
          this.archive.push(...response.data);
        })
        .catch((error) => {});
    },
    async getArchiveSize() {
      await axios
        .get(`/api/v1/gallery/count/`)
        .then((response) => {
          this.archiveSize = response.data.count;
        })
        .catch((error) => {});
    },
    async getSearchArchive() {
      axios.defaults.headers.common.Authorization = "";
      const start_index = this.searchArchive.length;
      const end_index = start_index + this.incrementSize;
      await this.getSearchArchiveSize();
      await axios
        .get(`/api/v1/search/${this.query}/${start_index}/${end_index}/`)
        .then((response) => {
          this.searchArchive.push(...response.data);
        })
        .catch((error) => {});
    },
    async getSearchArchiveSize() {
      await axios
        .get(`/api/v1/search/${this.query}/count/`)
        .then((response) => {
          this.searchArchiveSize = response.data.count;
        })
        .catch((error) => {});
    },
    removeLikes(archive) {
      for (let i = 0; i < archive.length; i++) {
        archive[i].image_is_liked = false;
      }
      return archive;
    },
    updateArchiveLikes(archive) {
      if (archive.length === 0) {
        return archive;
      }

      const email = localStorage.getItem("email");
      let start_index = archive.length - this.incrementSize;
      if (start_index < 0) {
        start_index = 0;
      }

      // The backend updates the element associated with the image we like.
      // However, clicking the 'load more' button does not retrieve the updated element.
      // Instead, it appends 10 new elements to the existing ones.
      // As a result, iterating through the entire archive may cause a bug where the image appears unliked.
      for (let i = start_index; i < archive.length; i++) {
        if (!archive[i]) {
          continue;
        }

        if (archive[i].liked_by_users) {
          if (archive[i].liked_by_users.includes(email)) {
            archive[i].image_is_liked = true;
          } else {
            archive[i].image_is_liked = false;
          }
        } else {
          archive[i].image_is_liked = false;
        }
      }
      return archive;
    },
    async logUserVisit() {
      const email = localStorage.getItem("email");
      if (email) {
        await axios.post("/api/v1/log_user_visit/", { email: email }).catch((error) => {
          console.error("Error logging user visit:", error);
        });
      }
    },
  },
};
</script>
