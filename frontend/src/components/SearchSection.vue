<template>
  <div class="container--fluid">
    <div class="position-relative d-flex flex-column">
      <img src="../assets/search_background.jpg" class="img-fluid custom-image" alt="...">

      <div class="container position-absolute top-50 start-50 translate-middle align-self-center">
        <div class="row px-5 pb-5">
          <div class="col">
            <h1 class="display-5 fs-1 fw-bold text-white">APOD</h1>
            <p class="fw-light text-white">Enter a date or keyword to search for an Astronomy Picture of the Day</p>
            <div class="input-group mb-3">
              <input
                type="text"
                class="form-control rounded-pill py-2 px-4"
                placeholder="Andromeda galaxy"
                v-model="searchQuery"
                @keydown.enter.prevent="search"
                aria-describedby="basic-addon1"
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchSection',
  components: {
  },
  data () {
    return {
      searchQuery: ''
    }
  },
  methods: {
    search () {
      console.log(this.searchQuery)
    }
  }
}
</script>

<style scoped>
  .custom-image {
    width: 100%;
    max-height: 500px;
    object-fit: cover;
    filter: brightness(0.5);
  }
</style>
