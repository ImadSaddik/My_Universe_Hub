<template>
  <div class="container">
    <div class="row my-1 my-sm-3">
      <div class="col d-flex justify-content-center">
        <h1 class="fs-4 fw-bold fs-sm-4 card-text">{{ item.title }}</h1>
      </div>
    </div>
    <div class="row mt-4 mt-sm-4 mt-lg-5">
      <div class="col d-flex justify-content-center">
        <img type="button" :src="item.image_url" class="img-fluid rounded-4" alt="" @click="downloadImage">
      </div>
    </div>
    <div class="row mt-4 mt-sm-4 mt-lg-5">
      <div class="col d-flex justify-content-center">
        <p class="custom-small-text fs-sm-6 card-text"><strong>Image credit:</strong> {{ item.authors }}</p>
      </div>
    </div>
    <div class="row mt-3 mt-lg-4 mb-3">
      <div class="col px-3">
        <p class="custom-small-text fs-sm-6 card-text" v-html="formatExplanation(formattedExplanation.prefix, formattedExplanation.content)"></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalBody',
  props: ['item'],
  components: {
  },
  computed: {
    formattedExplanation() {
      const explanation = this.item.explanation;
      const [prefix, ...contentParts] = explanation.split('Explanation:');
      const content = contentParts.join('Explanation:').trim();
      return {
        prefix: 'Explanation:',
        content: content
      };
    }
  },
  data () {
    return {
    }
  },
  methods: {
    downloadImage () {
      const imageUrl = this.item.image_url
      const anchorTag = document.createElement('a')
      anchorTag.href = imageUrl
      anchorTag.target = '_blank'

      document.body.appendChild(anchorTag)
      anchorTag.click()
      document.body.removeChild(anchorTag)
    },
    formatExplanation(prefix, content) {
      return `<strong>${prefix}</strong> ${content}`;
    }
  }
}
</script>

<style scoped>
.custom-small-text {
  font-size: 1rem;
}

@media (max-width: 576px) {
  .custom-small-text {
    font-size: 0.75rem;
  }
}
</style>
