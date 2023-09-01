<template>
  <div class="container-fluid mt-3">
    <div class="position-relative d-flex flex-column">
      <img src="../assets/search_background.jpg" class="img-fluid custom-image" alt="...">

      <div class="container position-absolute top-50 start-50 translate-middle align-self-center">
        <div class="row px-sm-5 pb-sm-5">
          <div class="col px-4">
            <h1 class="fs-4 fs-sm-1 fw-bold text-white">APOD</h1>
            <p class="fs-6 fw-light text-white">Enter a date or keyword to search for an Astronomy Picture of the Day</p>
            <div class="input-group mb-3">
              <input
                type="text"
                class="form-control rounded-3 py-1 py-sm-2 px-3 px-sm-4"
                placeholder="Andromeda galaxy"
                v-model="searchQuery"
                @keydown.enter.prevent="$emit('search', searchQuery)"
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
