<template>
  <div class="col py-3">
    <div v-for="(item, index) in archive.slice(sliceStart, sliceEnd)" :key="index" class="image-container mb-3">
      <img :src="item.image" v-lazy="item.image" class="img-fluid" alt="">
      <div class="overlay">
        <div class="overlay-content d-flex flex-column h-100">
          <div class="row align-items-center">
            <div class="col">
              <h5 class="card-subtitle">{{ item.title }}</h5>
            </div>
            <div class="col-auto">
              <i type="button" class="fa-solid fa-heart fa-xl" @click="likeImage(item)"></i>
            </div>
          </div>
          <div class="row flex-grow-1"></div>
          <div class="row align-items-center">
            <div class="col">
              <img src="../assets/apod_logo_white.svg" alt="">
            </div>
            <div class="col-auto">
              <i type="button" class="fa-solid fa-download fa-xl" @click="downloadImage(item)"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GalleryColumn',
  props: ['archive', 'sliceStart', 'sliceEnd'],
  components: {
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
      const imageUrl = item.image
      const anchorTag = document.createElement('a')
      anchorTag.href = imageUrl
      anchorTag.download = item.image

      document.body.appendChild(anchorTag)
      anchorTag.click()
      document.body.removeChild(anchorTag)
    }
  }
}
</script>

<style scoped>
.image-container {
  position: relative;
  display: inline-block;
}

.overlay {
  position: absolute;
  padding: 20px;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  display: none;
}

.image-container:hover .overlay {
  display: block;
}
</style>
