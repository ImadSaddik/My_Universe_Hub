<template>
  <section class="container-fluid">
    <div class="row">
      <div class="col pt-5 d-flex justify-content-center">
        <img :src="currentImage" class="img-fluid rounded-3" alt="" style="width: 70%;">
      </div>
      <div class="col p-5">
        <h5 class="fs-3 mb-4">Log In</h5>
        <form class="pe-5" @submit.prevent="submitForm">
          <div class="mb-3">
            <label for="exampleInputUsername" class="form-label">Username</label>
            <input type="text" class="form-control" id="exampleInputUsername" v-model="username">
          </div>
          <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">Password</label>
            <input class="form-control" id="exampleInputPassword1" v-model="password" :type="showHidePassword ? 'password' : 'text'">
          </div>
          <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" id="showHidePasswordCheckBox" @click="showHidePassword = !showHidePassword">
            <label class="form-check-label" for="showHidePasswordCheckBox">{{ showHidePassword ? 'Show password' : 'Hide password' }}</label>
          </div>
          <p>Or <a href="/signup">Click here</a>, if you don't have an account.</p>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LogInView',
  components: {
  },
  data () {
    return {
      images: ['Log_in_bg_1.jpg', 'Log_in_bg_2.jpg', 'Log_in_bg_3.jpg'],
      currentIndex: 0,
      username: '',
      password: '',
      showHidePassword: true
    }
  },
  computed: {
    currentImage () {
      return require(`@/assets/${this.images[this.currentIndex]}`)
    }
  },
  created () {
    this.imageInterval = setInterval(this.changeImage, 5000)
  },
  methods: {
    changeImage () {
      this.currentIndex = (this.currentIndex + 1) % this.images.length
    },
    async submitForm () {
      axios.defaults.headers.common.Authorization = ''
      localStorage.removeItem('token')

      const formData = {
        username: this.username,
        password: this.password
      }

      await axios
        .post('/api/v1/token/login', formData)
        .then(response => {
          const token = response.data.auth_token
          axios.defaults.headers.common.Authorization = 'Token ' + token

          localStorage.setItem('token', token)
          this.$store.dispatch('login', token)

          localStorage.setItem('username', this.username)
          this.$store.commit('setUsername', this.username)

          const toPath = this.$route.query.to || '/'
          this.$router.push(toPath)
          console.log('successfully logged in')
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  beforeUnmount () {
    clearInterval(this.imageInterval)
  }
}
</script>
