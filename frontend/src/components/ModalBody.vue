<template>
  <div class="container">
    <div class="row my-1 my-sm-3">
      <div class="col d-flex justify-content-center">
        <h1 data-testid="modal-title" class="custom-title-text">
          {{ item.title }}
        </h1>
      </div>
    </div>
    <div class="row mt-4 mt-sm-4 mt-lg-5">
      <div class="col d-flex justify-content-center">
        <img
          data-testid="modal-image"
          type="button"
          :src="item.image_url"
          class="img-fluid rounded-4"
          :alt="`APOD image: ${item.title} by ${item.authors}`"
          role="button"
          tabindex="0"
          @click="downloadImage"
          @keydown.enter="downloadImage"
        />
      </div>
    </div>
    <div class="row mt-4 mt-sm-4 mt-lg-5">
      <p data-testid="modal-image-credit" class="custom-small-text text-center my-0">
        <strong>Image credit:</strong> {{ item.authors }}
      </p>
    </div>
    <div class="row">
      <p class="custom-small-text my-0 text-center">
        <b data-testid="modal-posted-date">Posted:</b> {{ item.date }} on
        <a data-testid="modal-apod-link" href="https://apod.nasa.gov/" target="_blank" rel="noopener noreferrer"
          >APOD</a
        >
      </p>
    </div>
    <div class="row mt-3 mt-lg-4 mb-3">
      <div class="col px-sm-3">
        <p v-if="item.explanation" data-testid="modal-explanation" class="custom-small-text">
          <strong>Explanation:</strong>
          {{ item.explanation.substring(item.explanation.indexOf(":") + 1).trim() }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ModalBody",
  components: {},
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
  methods: {
    downloadImage() {
      const imageUrl = this.item.image_url;
      const anchorTag = document.createElement("a");
      anchorTag.href = imageUrl;
      anchorTag.target = "_blank";

      document.body.appendChild(anchorTag);
      anchorTag.click();
      document.body.removeChild(anchorTag);
    },
  },
};
</script>
