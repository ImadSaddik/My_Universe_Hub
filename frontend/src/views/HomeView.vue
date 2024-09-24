<template>
  <SearchSection @search="(query) => search(query)" />
  <GallerySection
    :archive="getUpdatedArchive"
    @selected-item="(value) => (selectedItem = value)"
    @increase-limit="increaseLimit()"
  />
  <BackToTopVue />
  <ImageDetails :item="selectedItem" />
</template>

<script>
import axios from "axios";
import SearchSection from "@/components/SearchSection.vue";
import GallerySection from "@/components/GallerySection.vue";
import BackToTopVue from "@/components/BackToTop.vue";
import ImageDetails from "@/components/ImageDetails.vue";

export default {
  name: "HomeView",
  components: {
    SearchSection,
    GallerySection,
    BackToTopVue,
    ImageDetails,
  },
  computed: {
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
  },
  data() {
    return {
      archive: [],
      searchArchive: [],
      selectedItem: "",
      incrementSize: 10,
      query: "",
    };
  },
  created() {
    this.$store.commit("setSelectedNavbarItem", "home");
  },
  mounted() {
    document.title = "My Universe Hub";
    this.getArchive();
  },
  methods: {
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
    async search(query) {
      this.query = query;

      if (query.trim().length === 0) {
        this.archive = [];
        this.searchArchive = [];
        
        await this.getArchive();
      } else {
        const start_index = this.searchArchive.length;
        const end_index = start_index + this.incrementSize;
        await axios
          .get(`/api/v1/search/${query}/${start_index}/${end_index}/`)
          .then((response) => {
            this.searchArchive.push(...response.data);
          })
          .catch((error) => {});
      }
    },
    async increaseLimit() {
      if (this.query.trim().length === 0) {
        await this.getArchive();
      } else {
        await this.search(this.query);
      }
    },
    removeLikes(archive) {
      for (let i = 0; i < archive.length; i++) {
        archive[i].image_is_liked = false;
      }
      return archive;
    },
    updateArchiveLikes(archive) {
      const email = localStorage.getItem("email");

      for (let i = 0; i < archive.length; i++) {
        if (archive[i].liked_by_users.includes(email)) {
          archive[i].image_is_liked = true;
        } else {
          archive[i].image_is_liked = false;
        }
      }
      return archive;
    },
  },
};
</script>
