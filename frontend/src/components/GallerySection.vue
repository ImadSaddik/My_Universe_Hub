<template>
  <div class="container-fluid mt-3">
    <div class="row gx-3">
      <GalleryColumn
        :archive="firstSublist"
        @selected-item="$emit('selected-item', $event)"
      />
      <GalleryColumn
        :archive="secondSublist"
        @selected-item="$emit('selected-item', $event)"
      />
      <GalleryColumn
        :archive="thirdSublist"
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
  data () {
    return {
      selectedItem: null,
      limit: 100,
      isHovering: false
    }
  },
  computed: {
    sublists () {
      const sublists = [[], [], []]

      for (let i = 0; i < this.limitedArchive.length; i++) {
        const sublistIndex = i % 3
        sublists[sublistIndex].push(this.limitedArchive[i])
      }

      return sublists
    },
    firstSublist () {
      return this.sublists[0]
    },
    secondSublist () {
      return this.sublists[1]
    },
    thirdSublist () {
      return this.sublists[2]
    },
    limitedArchive () {
      return this.archive.slice(0, this.limit)
    },
    showLoadMore () {
      return this.limit < this.archive.length
    }
  },
  methods: {
    increaseLimit () {
      this.limit += 100
    }
  }
}
</script>
