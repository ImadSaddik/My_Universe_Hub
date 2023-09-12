<template>
  <div class="container pt-2 pt-sm-5">
    <div v-if="data.image_url !== null">
      <div class="row my-3 d-flex flex-column">
        <div class="col d-flex justify-content-center">
          <h1 class="fs-4 card-text">{{ data.title }}</h1>
        </div>
        <div v-if="Object.keys(data).length" class="mt-2 col d-flex justify-content-center">
          {{ data.image_likes_count }}
          <div v-if="isLoggedIn">
            <i
              v-if="data.image_is_liked"
              type="button"
              class="ms-2 fa-solid fa-heart fa-xl me-3"
              style="color: #f66151;"
              @click="unlikeImage(data)"
            >
            </i>
            <i
              v-else
              type="button"
              class="ms-2 fa-regular fa-heart fa-xl me-3"
              @click="likeImage(data)"
            >
            </i>
          </div>
          <div v-else>
            <i
              :disabled="!isLoggedIn"
              class="ms-2 fa-regular fa-heart fa-xl me-3"
              style="color: #77767b;"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="Log in first to like this image"
            >
            </i>
          </div>
        </div>
      </div>
      <div class="row mt-4 mt-sm-5">
        <div class="col d-flex justify-content-center">
          <img type="button" :src="data.image_url" class="img-fluid rounded-4" alt="" @click="downloadImage">
        </div>
      </div>
      <div class="row mt-4 mt-sm-5 mb-3">
        <div class="col px-3">
          <p class="card-text">{{ data.explanation }}</p>
        </div>
      </div>
    </div>
    <div v-else class="row d-flex align-items-center justify-content-center" style="height: calc(80vh);">
      <h5 class="nav-link text-center">No image for today 😔, see you tomorrow</h5>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TodayPictureView',
  components: {
  },
  computed: {
    isLoggedIn () {
      return this.$store.state.token !== ''
    },
    getUsername () {
      return this.$store.state.username
    }
  },
  data () {
    return {
      data: {}
    }
  },
  mounted () {
    this.getTodayPicture()
    document.title = 'Today\'s Picture'
  },
  methods: {
    async getTodayPicture () {
      await axios
        .get('/api/v1/today/')
        .then(response => {
          const username = this.getUsername
          console.log(username)
          this.data = response.data
          console.log(response.data)

          if (username) {
            this.data.image_is_liked = response.data.liked_by_users.includes(username)
          }
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
    },
    async likeImage (item) {
      const data = JSON.stringify({
        date: item.date,
        username: this.getUsername
      })

      await axios
        .post('/api/v1/like_image/', data, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': 'csrftoken'
          }
        })
        .then(response => {
          console.log(response)
          item.image_is_liked = true
          item.image_likes_count += 1
        })
        .catch(error => {
          console.log(error)
        })
    },
    async unlikeImage (item) {
      const data = JSON.stringify({
        date: item.date,
        username: this.getUsername
      })

      await axios
        .post('/api/v1/unlike_image/', data, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': 'csrftoken'
          }
        })
        .then(response => {
          console.log(response)
          item.image_is_liked = false
          item.image_likes_count -= 1
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>
