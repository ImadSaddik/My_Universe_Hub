<template>
  <div class="container-fluid m-0 p-3">
    <div class="position-relative d-flex flex-column">
      <img src="../assets/search_background.jpg" class="img-fluid custom-image" alt="...">

      <div class="container position-absolute top-50 start-50 translate-middle align-self-center">
        <div class="row px-sm-5 pb-sm-5">
          <div class="col px-4 px-sm-4">
            <h1 class="fs-5 fs-sm-1 fw-bold text-white">Universe hub</h1>
            <p class="custom-small-text fs-sm-6 fw-light text-white">Discover images by entering keywords separated by commas. Find the image you are looking for.</p>
            <div class="input-container">
              <i class="fas fa-search input-icon"></i>
              <input
                type="text"
                class="input-field"
                placeholder="Andromeda galaxy"
                v-model="searchQuery"
                @keydown.enter.prevent="$emit('search', searchQuery)"
                aria-describedby="basic-addon1"
              />
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

.custom-small-text {
  font-size: 1rem;
}

@media (max-width: 576px) {
  .custom-small-text {
    font-size: 0.75rem;
  }
  .custom-image {
    min-height: 300px;
  }
}
</style>
