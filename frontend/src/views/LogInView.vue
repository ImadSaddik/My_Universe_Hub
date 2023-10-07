<template>
  <section class="container-fluid" style="height: calc(100vh - 70px)">
    <div class="position-relative h-100 d-flex flex-column">
      <img src="../assets/Log_in_bg.jpg" class="img-fluid custom-image" alt="...">

      <div class="container position-absolute top-50 start-50 translate-middle align-self-center">
        <div class="row px-2 px-sm-5 pb-5 d-flex justify-content-center">
          <div class="col col-sm-6">
            <h1 class="display-5 fs-1 fw-bold text-white mb-4">Log In</h1>
            <div v-if="showAlertDialog" class="alert alert-warning alert-dismissible fade show rounded-3" role="alert">
              <strong>Error! </strong> {{ errorMessage }}
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="showAlertDialog = false"></button>
            </div>
            <form @submit.prevent="submitForm">
              <div class="input-group input-group-sm mb-3">
                <input
                  type="text"
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="Your username"
                  v-model="username"
                >
              </div>
              <div class="input-group input-group-sm mb-3">
                <input
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="Your password"
                  v-model="password"
                  :type="showHidePassword ? 'password' : 'text'"
                >
              </div>
              <div class="mb-3 form-check">
                <label
                  class="form-check-label text-white"
                  for="showHidePasswordCheckBox"
                >
                {{ showHidePassword ? 'Show password' : 'Hide password' }}
                </label>
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="showHidePasswordCheckBox"
                  @click="showHidePassword = !showHidePassword"
                >
              </div>
              <p class="text-white">Forgot password? <a href="/reset_password">Click here</a></p>
              <p class="text-white">Or <a href="/signup">Click here</a>, if you don't have an account.</p>
              <button type="submit" class="btn btn-primary">Submit</button>
            </form>
          </div>
        </div>
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
  mounted () {
    document.title = 'Log In'
  },
  data () {
    return {
      username: '',
      password: '',
      showHidePassword: true,
      showAlertDialog: false,
      errorMessage: ''
    }
  },
  methods: {
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

          localStorage.setItem('selectedNavbarItem', 'home')
          this.$store.commit('setSelectedNavbarItem', 'home')

          this.$router.push({ name: 'home', replace: true })
          console.log('successfully logged in')
        })
        .catch(error => {
          console.log(error)
          this.showAlertDialog = true
          this.errorMessage = 'Invalid username or password.'
        })
    }
  }
}
</script>

<style scoped>
  .custom-image {
    height: 100%;
    object-fit: cover;
    filter: brightness(0.4);
  }
</style>
