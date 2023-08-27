<template>
  <div class="container">
    <div class="row my-3">
      <div class="col d-flex justify-content-center">
        <h1 class="fs-4 card-text">{{ item.title }}</h1>
      </div>
    </div>
    <div class="row mt-5">
      <div class="col d-flex justify-content-center">
        <img type="button" :src="item.image_url" class="img-fluid rounded-4" alt="" @click="downloadImage">
      </div>
    </div>
    <div class="row mt-5 mb-3">
      <div class="col px-3">
        <p class="card-text">{{ item.explanation }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalBody',
  props: ['item'],
  components: {
  },
  data () {
    return {
    }
  },
  methods: {
    downloadImage () {
      const imageUrl = this.item.image_url
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
