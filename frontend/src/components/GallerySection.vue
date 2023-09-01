<template>
  <div class="container-fluid mt-3">
    <div class="row gx-3">
      <GalleryColumn
        v-for="(sublist, index) in sublists"
        :key="index"
        :archive="sublist"
        @selected-item="$emit('selected-item', $event)"
      />
    </div>
    <div v-if="showLoadMore" class="row mx-0 mb-3">
      <div
        type="button"
        class="col border py-4 d-flex align-items-center justify-content-center"
        :class="{ 'border-dark': isHovering }"
        @mouseover="isHovering = true"
        @mouseleave="isHovering = false"
        @click="increaseLimit"
      >
        Load more
      </div>
    </div>
  </div>
</template>

<script>
import GalleryColumn from './GalleryColumn.vue'

export default {
  name: 'GallerySection',
  props: ['archive'],
  components: {
    GalleryColumn
  },
  computed: {
    sublists () {
      const sublists = []
      for (let i = 0; i < this.numberOfSublists; i++) {
        sublists.push([])
      }

      for (let i = 0; i < this.limitedArchive.length; i++) {
        const sublistIndex = i % this.numberOfSublists
        sublists[sublistIndex].push(this.limitedArchive[i])
      }

      return sublists
    },
    limitedArchive () {
      return this.archive.slice(0, this.limit)
    },
    showLoadMore () {
      return this.limit < this.archive.length
    }
  },
  data () {
    return {
      selectedItem: null,
      limit: 100,
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
    window.addEventListener('resize', () => {
      this.screenWidth = window.innerWidth
      if (this.screenWidth >= this.breakPoints.lg) {
        this.numberOfSublists = 3
      } else if (this.screenWidth < this.breakPoints.lg && this.screenWidth >= this.breakPoints.sm) {
        this.numberOfSublists = 2
      } else {
        this.numberOfSublists = 1
      }
    })
  },
  methods: {
    increaseLimit () {
      this.limit += 100
    }
  }
}
</script>
