<template>
  <div class="container">
    <div class="row my-1 my-sm-3">
      <div class="col d-flex justify-content-center">
        <h1 class="custom-title-text">{{ item.title }}</h1>
      </div>
    </div>
    <div class="row mt-4 mt-sm-4 mt-lg-5">
      <div class="col d-flex justify-content-center">
        <img
          type="button"
          :src="item.image_url"
          class="img-fluid rounded-4"
          alt=""
          @click="downloadImage"
        />
      </div>
    </div>
    <div class="row mt-4 mt-sm-4 mt-lg-5">
      <p class="custom-small-text text-center my-0">
        <strong>Image credit:</strong> {{ item.authors }}
      </p>
    </div>
    <div class="row">
      <p class="custom-small-text my-0 text-center">
          <b>Posted:</b> {{ item.date }} on
          <a
            href="https://apod.nasa.gov/"
            target="_blank"
            rel="noopener noreferrer"
            >APOD</a
          >
        </p>
    </div>
    <div class="row mt-3 mt-lg-4 mb-3">
      <div class="col px-sm-3">
        <p
          class="custom-small-text"
          v-html="formatExplanation(item.explanation)"
        ></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ModalBody",
  props: ["item"],
  components: {},
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
    formatExplanation(explanation) {
      if (!explanation) {
        return "";
      }
      explanation = explanation.trim();
      const [_, ...contentParts] = explanation.split("Explanation:");

      const content = contentParts.join("Explanation:").trim();
      const prefix = "Explanation:";

      return `<strong>${prefix}</strong> ${content}`;
    },
  },
};
</script>
