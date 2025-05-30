<template>
  <section class="container-fluid" style="height: 3.5rem">
    <div class="row row-background h-100 d-flex align-items-center">
      <p class="marquee custom-small-text p-0 m-0 text-center">
        <span>
          This website is a redesign of the Astronomy Picture of the Day (APOD). Images are credited to their respective
          astrophotographers. For more details, visit
          <a data-test="apod-link" href="https://apod.nasa.gov/" target="_blank" rel="noopener noreferrer">APOD</a>.
        </span>
      </p>
    </div>
  </section>
</template>

<script>
export default {
  name: "AcknowledgementBar",
};
</script>

<style scoped>
.row-background {
  background-color: white;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.15);
}

@media (max-width: 1200px) {
  .marquee {
    margin: 0 auto;
    white-space: nowrap;
    overflow: hidden;
    position: absolute;
    width: 100%;
  }

  .marquee span {
    display: inline-block;
    padding-left: 100%;
    animation: marquee 10s linear infinite;
  }

  @keyframes marquee {
    0% {
      transform: translate(0, 0);
    }
    100% {
      transform: translate(-100%, 0);
    }
  }
}
</style>
