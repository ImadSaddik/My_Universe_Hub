<template>
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <img src="../assets/galaxy_logo.svg" alt="" style="width: 3rem;">
          <div class="col d-flex align-items-center justify-content-end">
            {{item.image_likes_count}}
            <div v-if="item.image_is_liked">
              <i
                type="button"
                class="ms-2 fa-solid fa-heart fa-xl me-3"
                style="color: #f66151;"
                @click="unlikeImage(item)"
              >
              </i>

            </div>
            <div v-else>
              <i
                v-if="isLoggedOff"
                :disabled="isLoggedOff"
                class="ms-2 fa-regular fa-heart fa-xl me-3"
                style="color: #77767b;"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                data-bs-title="Log in first to like this image"
              >
              </i>
              <i
                v-else
                type="button"
                class="ms-2 fa-regular fa-heart fa-xl me-3"
                @click="likeImage(item)"
              >
              </i>
            </div>

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
import axios from 'axios'
import ModalBody from './ModalBody.vue'

export default {
  name: 'ImageDetails',
  props: ['item'],
  components: {
    ModalBody
  },
  computed: {
    isLoggedOff () {
      return this.$store.state.token === ''
    },
    getEmail() {
      return this.$store.state.email;
    },
  },
  data () {
    return {
    }
  },
  methods: {
    async likeImage (item) {
      const data = JSON.stringify({
        date: item.date,
        email: localStorage.getItem('email')
      })

      await axios
        .post('/api/v1/like_image/', data, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': 'csrftoken'
          }
        })
        .then(response => {
          item.image_is_liked = true
          item.image_likes_count += 1
        })
        .catch(error => {
        })
    },
    async unlikeImage (item) {
      this.$emit('unlike-image', item)
      const data = JSON.stringify({
        date: item.date,
        email: this.getEmail
      })

      await axios
        .post('/api/v1/unlike_image/', data, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': 'csrftoken'
          }
        })
        .then(response => {
          item.image_is_liked = false
          item.image_likes_count -= 1
        })
        .catch(error => {
        })
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
