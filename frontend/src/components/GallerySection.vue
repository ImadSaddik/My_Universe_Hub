<template>
  <div class="container-fluid m-0 py-0 px-3">
    <div v-if="searchResultCount == 0">
      <div class="row d-flex align-items-center justify-content-center" style="height: calc(20vh);">
        <h5 class="nav-link text-center">
          No images found for the search query 😔, try another one.
        </h5>
      </div>
    </div>
    <div v-else>
      <div class="row gx-3">
        <GalleryColumn
          v-for="(sublist, index) in sublists"
          :key="index"
          :archive="sublist"
          @selected-item="$emit('selected-item', $event)"
        />
      </div>
      <div class="row mx-0 mb-3">
        <div
          v-if="shouldShowLoadMoreButton"
          type="button"
          class="col custom-btn custom-btn-white py-4 d-flex align-items-center justify-content-center"
          :class="{ 'border-dark': isHovering }"
          @mouseover="isHovering = true"
          @mouseleave="isHovering = false"
          @click="increaseLimit"
        >
          Load more
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import GalleryColumn from './GalleryColumn.vue'

export default {
  name: 'GallerySection',
  props: ['archive', 'shouldShowLoadMoreButton', "searchResultCount"],
  components: {
    GalleryColumn
  },
  computed: {
    sublists () {
      const sublists = []
      for (let i = 0; i < this.numberOfSublists; i++) {
        sublists.push([])
      }

      for (let i = 0; i < this.archive.length; i++) {
        const sublistIndex = i % this.numberOfSublists
        sublists[sublistIndex].push(this.archive[i])
      }

      return sublists
    },
    isArchiveEmpty () {
      return this.archive.length === 0
    }
  },
  data () {
    return {
      selectedItem: null,
      isHovering: false,
      screenWidth: window.innerWidth,
      breakPoints: {
        lg: 992,
        sm: 576
      },
      numberOfSublists: 3
    }
  },
  mounted () {
    window.addEventListener('resize', this.handleWindowResize)
  },
  beforeUnmount () {
    window.removeEventListener('resize', this.handleWindowResize)
  },
  methods: {
    increaseLimit () {
      this.$emit('increaseLimit')
    },
    handleWindowResize () {
      this.screenWidth = window.innerWidth
      if (this.screenWidth >= this.breakPoints.lg) {
        this.numberOfSublists = 3
      } else if (this.screenWidth < this.breakPoints.lg && this.screenWidth >= this.breakPoints.sm) {
        this.numberOfSublists = 2
      } else {
        this.numberOfSublists = 1
      }
    }
  }
}
</script>
