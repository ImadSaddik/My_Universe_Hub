<template>
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <img src="../assets/apod_logo.svg" alt="">
          <div class="col d-flex align-items-center justify-content-end">
            <i type="button" class="fa-regular fa-heart fa-xl me-3" @click="likeImage(item)"></i>
            <i type="button" class="fa-solid fa-download fa-xl me-3" @click="downloadImage(item)"></i>
            <i type="button" class="fa-solid fa-xmark fa-2xl" data-bs-dismiss="modal"></i>
          </div>
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
    likeImage (item) {
      console.log(item)
    },
    downloadImage (item) {
      const imageUrl = item.image_url
      const anchorTag = document.createElement('a')
      anchorTag.href = imageUrl
      anchorTag.target = '_blank'

      document.body.appendChild(anchorTag)
      anchorTag.click()
      document.body.removeChild(anchorTag)
    }
  }
}
</script>
