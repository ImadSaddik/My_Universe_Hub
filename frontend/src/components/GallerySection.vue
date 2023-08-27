<template>
  <div class="container-fluid mt-3">
    <div class="row gx-3">
      <GalleryColumn
        :archive="limitedArchive"
        :sliceStart="0"
        :sliceEnd="Math.ceil(limitedArchive.length / 3)"
        @selected-item="$emit('selected-item', $event)"
      />
      <GalleryColumn
        :archive="limitedArchive"
        :sliceStart="Math.ceil(limitedArchive.length / 3)"
        :sliceEnd="Math.ceil(2 * limitedArchive.length / 3)"
        @selected-item="$emit('selected-item', $event)"
      />
      <GalleryColumn
        :archive="limitedArchive"
        :sliceStart="Math.ceil(2 * limitedArchive.length / 3)"
        :sliceEnd="limitedArchive.length"
        @selected-item="$emit('selected-item', $event)"
      />
    </div>
    <div v-if="showLoadMore" class="row mx-0 mb-3">
      <div type="button" class="col border py-4 d-flex align-items-center justify-content-center" @click="increaseLimit">
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
      limit: 100
    }
  },
  computed: {
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
