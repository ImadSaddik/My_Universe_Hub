<template>
  <ApodStatusOverlay />

  <div v-if="apodStatus === 'up'" class="mt-3">
    <GallerySection
      :archive="getArchive"
      :should-show-load-more-button="shouldShowLoadMoreButton"
      @selected-item="(value) => (selectedItem = value)"
      @increase-limit="increaseLimit()"
    />
    <BackToTopVue />
    <ImageDetails :item="selectedItem" />
  </div>
</template>

<script>
import axios from "axios";
import GallerySection from "@/components/GallerySection.vue";
import BackToTopVue from "@/components/BackToTop.vue";
import ImageDetails from "@/components/ImageDetails.vue";
import ApodStatusOverlay from "@/components/ApodStatusOverlay.vue";

export default {
  name: "TrendingView",
  components: {
    GallerySection,
    BackToTopVue,
    ImageDetails,
    ApodStatusOverlay,
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
    apodStatus() {
      return this.$store.state.apodStatus;
    },
    getArchive() {
      if (this.isUserLoggedOff) {
        return this.removeLikes();
      } else {
        return this.updateArchiveLikes();
      }
    },
    isUserLoggedOff() {
      return this.$store.state.token === "";
    },
    shouldShowLoadMoreButton() {
      return this.archive.length < this.archiveFullSize;
    },
  },
  watch: {
    apodStatus(newStatus, oldStatus) {
      if (newStatus === "up" && oldStatus !== "up") {
        this.getTrendingArchive();
        this.getTrendingArchiveSize();
      }
    },
  },
  created() {
    document.title = "Trending";
  },
  async mounted() {
    if (this.apodStatus === "up") {
      await this.getTrendingArchive();
      await this.getTrendingArchiveSize();
    }
  },
  methods: {
    async getTrendingArchive() {
      const start_index = this.archive.length;
      const end_index = start_index + this.incrementSize;
      await axios
        .get(`/api/v1/trending/${start_index}/${end_index}/`)
        .then((response) => {
          this.archive.push(...response.data);
        })
        .catch((error) => {
          this.$store.commit("addErrorMessage", "Failed to fetch trending archive");
        });
    },
    async getTrendingArchiveSize() {
      await axios
        .get("/api/v1/trending/count/")
        .then((response) => {
          this.archiveFullSize = response.data.count;
        })
        .catch((error) => {
          this.$store.commit("addErrorMessage", "Failed to fetch trending archive size");
        });
    },
    async increaseLimit() {
      await this.getTrendingArchive();
    },
    removeLikes() {
      for (let i = 0; i < this.archive.length; i++) {
        this.archive[i].image_is_liked = false;
      }
      return this.archive;
    },
    updateArchiveLikes() {
      const email = localStorage.getItem("email");
      for (let i = 0; i < this.archive.length; i++) {
        if (this.archive[i].liked_by_users.includes(email)) {
          this.archive[i].image_is_liked = true;
        } else {
          this.archive[i].image_is_liked = false;
        }
      }
      return this.archive;
    },
  },
};
</script>
