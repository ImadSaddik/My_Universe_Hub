<template>
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <img src="../assets/apod_logo.svg" alt="">
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <ModalBody :item="item" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ModalBody from './ModalBody.vue'

export default {
  name: 'ImageDetails',
  props: ['item'],
  components: {
    ModalBody
  },
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>
