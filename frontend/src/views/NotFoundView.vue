<template>
  <div>
    <h1>404 - Page Not Found</h1>
    <p>Sorry, the page you are looking for does not exist.</p>
    <router-link to="/">Go back to Home</router-link>
  </div>
</template>

<script>
export default {
  name: "NotFoundView",
};
</script>

<style scoped>
div {
  text-align: center;
  margin-top: 2rem;
}
</style>
