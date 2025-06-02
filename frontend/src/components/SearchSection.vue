<template>
  <div class="container-fluid m-0 p-3">
    <div class="position-relative d-flex flex-column">
      <img
        data-cy="background-image"
        src="../assets/home_page/search_background.jpg"
        class="img-fluid custom-image"
        alt="..."
      />

      <div class="container position-absolute top-50 start-50 translate-middle align-self-center">
        <div class="row px-sm-5 pb-sm-5">
          <div class="col px-4 px-sm-4">
            <h1 data-cy="hero-title" class="title-text text-white">My Universe Hub</h1>
            <p data-cy="hero-description" class="description-text text-white">
              Discover images by entering keywords separated by commas. Find the image you are looking for.
            </p>
            <div class="input-container">
              <i class="fas fa-search input-icon" />
              <input
                v-model="searchQuery"
                data-cy="search-input"
                type="text"
                class="input-field"
                placeholder="Andromeda, Jupiter, Pluto, M31"
                aria-describedby="basic-addon1"
                @keydown.enter.prevent="$emit('search', searchQuery)"
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
  name: "SearchSection",
  components: {},
  emits: ["search"],
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {},
};
</script>

<style scoped>
.custom-image {
  width: 100%;
  max-height: 500px;
  object-fit: cover;
  filter: brightness(0.5);
}

.description-text {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  font-weight: 300;
}

.title-text {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  font-weight: bold;
}

@media (max-width: 768px) {
  .custom-image {
    min-height: 300px;
  }

  .description-text {
    font-size: 1rem;
    margin-bottom: 1rem;
  }

  .title-text {
    font-size: 1.5rem;
  }
}
</style>
