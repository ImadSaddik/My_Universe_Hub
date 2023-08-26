<template>
  <div class="container-fluid mt-3">
    <div class="row gx-3">
      <GalleryColumn
        :archive="archive"
        :sliceStart="0"
        :sliceEnd="Math.floor(archive.length / 3)"
      />
      <GalleryColumn
        :archive="archive"
        :sliceStart="Math.floor(archive.length / 3)"
        :sliceEnd="Math.floor(2 * archive.length / 3)"
      />
      <GalleryColumn
        :archive="archive"
        :sliceStart="Math.floor(2 * archive.length / 3)"
        :sliceEnd="archive.length"
      />
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
    }
  },
  methods: {
  }
}
</script>
