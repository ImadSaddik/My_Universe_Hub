<template>
  <div class="container pt-5">
    <div class="row my-3">
      <div class="col d-flex justify-content-center">
        <h1 class="fs-4 card-text">{{ data.title }}</h1>
      </div>
    </div>
    <div class="row mt-5">
      <div class="col d-flex justify-content-center">
        <img type="button" :src="data.image_url" class="img-fluid rounded-4" alt="" @click="downloadImage">
      </div>
    </div>
    <div class="row mt-5 mb-3">
      <div class="col px-3">
        <p class="card-text">{{ data.explanation }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TodayPictureView',
  components: {
  },
  data () {
    return {
      data: {}
    }
  },
  mounted () {
    this.getTodayPicture()
  },
  methods: {
    async getTodayPicture () {
      await axios
        .get('/api/v1/today/')
        .then(response => {
          this.data = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    downloadImage () {
      const imageUrl = this.data.image_url
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
