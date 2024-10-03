<template>
  <div
    class="modal fade"
    id="exampleModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <img
            class="image-logo"
            src="../assets/logos/galaxy_logo.svg"
            alt=""
          />
          <div class="col d-flex align-items-center justify-content-end">
            <div v-if="isLoggedIn" class="me-2 me-sm-3">
              <div
                v-if="item.image_is_liked"
                class="like-icon-container d-flex align-items-center"
                @click="unlikeImage(item)"
              >
                {{ item.image_likes_count }}
                <i
                  type="button"
                  class="ms-2 fa-solid fa-heart fa-xl"
                  style="color: #f66151"
                >
                </i>
              </div>
              <div
                v-else
                class="like-icon-container d-flex align-items-center"
                @click="likeImage(item)"
              >
                {{ item.image_likes_count }}
                <i type="button" class="ms-2 fa-regular fa-heart fa-xl"> </i>
              </div>
            </div>
            <div v-else class="me-2 me-sm-3">
              <div class="like-icon-container d-flex align-items-center">
                {{ item.image_likes_count }}
                <i
                  :disabled="!isLoggedIn"
                  class="ms-2 fa-regular fa-heart fa-xl"
                  style="color: #77767b"
                >
                </i>
              </div>
            </div>

            <i
              type="button"
              class="fa-solid fa-download fa-xl me-2 me-sm-3"
              @click="downloadImage(item)"
            ></i>
            <i
              type="button"
              class="fa-solid fa-xmark fa-2xl"
              data-bs-dismiss="modal"
            ></i>
          </div>
        </div>
        <div class="modal-body">
          <ModalBody :item="item" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ModalBody from "./ModalBody.vue";

export default {
  name: "ImageDetails",
  props: ["item"],
  components: {
    ModalBody,
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.token !== "";
    },
    getEmail() {
      return this.$store.state.email;
    },
  },
  data() {
    return {};
  },
  methods: {
    async likeImage(item) {
      const data = JSON.stringify({
        date: item.date,
        email: localStorage.getItem("email"),
      });

      await axios
        .post("/api/v1/like_image/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          item.image_is_liked = true;
          item.image_likes_count += 1;
        })
        .catch((error) => {});
    },
    async unlikeImage(item) {
      this.$emit("unlike-image", item);
      const data = JSON.stringify({
        date: item.date,
        email: this.getEmail,
      });

      await axios
        .post("/api/v1/unlike_image/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          item.image_is_liked = false;
          item.image_likes_count -= 1;
        })
        .catch((error) => {});
    },
    downloadImage(item) {
      const imageUrl = item.image_url;
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

<style scoped>
.image-logo {
  height: 2rem;
}

.like-icon-container {
  padding: 0.5rem 1rem 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
}

.like-icon-container:hover {
  background-color: #f0f0f0;
}
</style>
