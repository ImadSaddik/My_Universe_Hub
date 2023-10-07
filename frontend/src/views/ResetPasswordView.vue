<template>
  <section class="container-fluid" style="height: calc(100vh - 70px)">
    <div class="position-relative h-100 d-flex flex-column">
      <img src="../assets/Sign_up_bg.jpg" class="img-fluid custom-image" alt="...">

      <div class="container position-absolute top-50 start-50 translate-middle align-self-center">
        <div class="row px-2 px-sm-5 pb-5 d-flex justify-content-center">
          <div class="col col-sm-6">
            <h1 class="display-5 fs-1 fw-bold text-white mb-4">Reset password</h1>

            <div v-if="showErrorDialog" class="alert alert-warning alert-dismissible fade show rounded-3" role="alert">
              <div v-for="error in errors" :key="error">
                <strong>Error! </strong> {{ error }}
              </div>
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="showErrorDialog = false"></button>
            </div>

            <form @submit.prevent="submitForm">
              <div class="input-group input-group-sm mb-3">
                <input
                  type="text"
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="Username"
                  id="exampleInputUsername"
                  v-model="username">
              </div>
              <div class="input-group input-group-sm mb-3">
                <input
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="New password"
                  id="exampleInputPassword1"
                  v-model="password"
                  :type="showHidePassword ? 'password' : 'text'">
              </div>
              <div class="input-group input-group-sm mb-3">
                <input
                  class="form-control rounded-3 py-2 px-3"
                  placeholder="Repeat new password"
                  id="exampleInputPassword2"
                  v-model="repeatPassword"
                  :type="showHidePassword ? 'password' : 'text'">
              </div>
              <div class="mb-3 form-check">
                <label class="form-check-label text-white" for="showHidePasswordCheckBox">{{ showHidePassword ? 'Show password' : 'Hide password' }}</label>
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="showHidePasswordCheckBox"
                  @click="showHidePassword = !showHidePassword">
              </div>
              <p class="text-white">Or <a href="/login">Click here</a>, to go back to the log in page.</p>
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
  name: 'ResetPasswordView',
  components: {
  },
  mounted () {
    document.title = 'Reset Password'
  },
  data () {
    return {
      username: '',
      password: '',
      repeatPassword: '',

      errors: [],

      showErrorDialog: false,
      showHidePassword: true
    }
  },
  methods: {
    async submitForm () {
      if (this.errorExist()) {
        return
      }

      const resetData = JSON.stringify({
        username: this.username,
        newPassword: this.password
      })

      await axios
        .post('/api/v1/reset_password/', resetData, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': 'csrftoken'
          }
        })
        .then((response) => {
          this.showErrorDialog = false

          this.$router.push('/login')
          console.log('successfully signed up')
        })
        .catch((error) => {
          console.log(error)
          this.errors.push(error.response.data)
          this.showErrorDialog = true
        })
    },
    errorExist () {
      this.errors = []

      if (this.username === '') {
        this.errors.push('The username field is required.')
      }

      if (this.password === '') {
        this.errors.push('The password field is required.')
      }

      if (this.repeatPassword === '') {
        this.errors.push('The repeat password field is required.')
      }

      if (this.password !== this.repeatPassword) {
        this.errors.push('The two password fields didn\'t match.')
      }

      if (this.errors.length) {
        this.showErrorDialog = true
        return true
      }
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
