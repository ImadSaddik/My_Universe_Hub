<template>
  <section class="container-fluid">
    <div class="row">
      <div class="col pt-5 d-flex justify-content-center">
        <img :src="currentImage" class="img-fluid rounded-3" alt="" style="width: 70%;">
      </div>
      <div class="col p-5">
        <h5 class="fs-3 mb-4">Sign up</h5>
        <form class="pe-5" @submit.prevent="submitForm">
          <div class="mb-3">
            <label for="exampleInputUsername" class="form-label">Username</label>
            <input type="text" class="form-control" id="exampleInputUsername" v-model="username">
          </div>
          <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">Password</label>
            <input class="form-control" id="exampleInputPassword1" v-model="password" :type="showHidePassword ? 'password' : 'text'">
          </div>
          <div class="mb-3">
            <label for="exampleInputPassword2" class="form-label">Repeat password</label>
            <input class="form-control" id="exampleInputPassword2" v-model="repeatPassword" :type="showHidePassword ? 'password' : 'text'">
          </div>
          <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" id="showHidePasswordCheckBox" @click="showHidePassword = !showHidePassword">
            <label class="form-check-label" for="showHidePasswordCheckBox">{{ showHidePassword ? 'Show password' : 'Hide password' }}</label>
          </div>
          <p>Or <a href="/login">Click here</a>, if you already have an account.</p>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SignUpView',
  components: {
  },
  data () {
    return {
      images: ['Log_in_bg_1.jpg', 'Log_in_bg_2.jpg', 'Log_in_bg_3.jpg'],
      currentIndex: 0,
      username: '',
      password: '',
      repeatPassword: '',
      showHidePassword: true,
      errors: []
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
      this.errors = []

      if (this.username === '') {
        this.errors.push('The username field is required.')
      }

      if (this.password === '') {
        this.errors.push('The password field is required.')
      }

      if (this.password !== this.repeatPassword) {
        this.errors.push('The two password fields didn\'t match.')
      }

      if (!this.errors.length) {
        const formData = {
          username: this.username,
          password: this.password
        }

        axios.defaults.headers.common.Authorization = ''
        await axios
          .post('/api/v1/users/', formData)
          .then(response => {
            this.$router.push('/login')
            console.log('successfully signed up')
          })
          .catch(error => {
            console.log(error)
          })
      }
    }
  },
  beforeUnmount () {
    clearInterval(this.imageInterval)
  }
}
</script>
