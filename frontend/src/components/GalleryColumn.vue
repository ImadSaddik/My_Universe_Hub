<template>
  <div class="col-12 col-sm-6 col-lg-4 py-0">
    <div v-for="(item, index) in archive" :key="index" data-testid="gallery-item" class="mb-3">
      <div>
        <img
          v-lazy="item.image_url"
          data-testid="gallery-item-image"
          :src="item.image_url"
          class="img-fluid image-container"
          :alt="`APOD image: ${item.title} by ${item.authors}`"
          data-bs-toggle="modal"
          data-bs-target="#exampleModal"
          role="button"
          tabindex="0"
          @click="$emit('selectedItem', item)"
          @keydown.enter="selectAndShowModal(item)"
        />
        <div class="row m-0">
          <div class="col py-1 d-flex align-items-center marquee-container">
            <img
              data-testid="gallery-item-app-logo"
              src="../assets/logos/galaxy_logo.svg"
              alt="MyUniverseHub galaxy logo"
              style="width: 2rem"
            />
            <p data-testid="gallery-item-title" class="custom-small-text m-0 ms-3 fw-bold">
              {{ item.title }}
            </p>
          </div>
          <div data-testid="gallery-item-action" class="col-auto p-0 py-1">
            <div v-if="isLoggedIn">
              <div
                v-if="item.image_is_liked"
                data-testid="gallery-item-unlike-or-like"
                class="like-icon-container d-flex align-items-center"
                role="button"
                tabindex="0"
                @click="unlikeImage(item)"
                @keydown.enter="unlikeImage(item)"
              >
                {{ item.image_likes_count }}
                <i type="button" class="ms-2 fa-solid fa-heart fa-xl" style="color: #f66151" />
              </div>
              <div
                v-else
                data-testid="gallery-item-unlike-or-like"
                class="like-icon-container d-flex align-items-center"
                role="button"
                tabindex="0"
                @click="likeImage(item)"
                @keydown.enter="likeImage(item)"
              >
                {{ item.image_likes_count }}
                <i type="button" class="ms-2 fa-regular fa-heart fa-xl" />
              </div>
            </div>
            <div v-else>
              <div data-testid="gallery-item-unlike-or-like" class="like-icon-container d-flex align-items-center">
                {{ item.image_likes_count }}
                <i :disabled="!isLoggedIn" class="ms-2 fa-regular fa-heart fa-xl" style="color: #77767b" />
              </div>
            </div>
          </div>
        </div>
        <div>
          <p data-testid="gallery-item-image-credit" class="custom-small-text">
            <b>Image credit:</b> {{ item.authors }}
          </p>
          <p class="custom-small-text">
            <b data-testid="gallery-item-date">Posted:</b> {{ item.date }} on
            <a
              data-testid="gallery-item-apod-link"
              href="https://apod.nasa.gov/"
              target="_blank"
              rel="noopener noreferrer"
              >APOD</a
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "GalleryColumn",
  components: {},
  props: {
    archive: {
      type: Array,
      required: true,
    },
  },
  emits: ["unlike-image", "selectedItem"],
  data() {
    return {
      selectedItem: null,
    };
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.token !== "";
    },
    getEmail() {
      return this.$store.state.email;
    },
  },
  methods: {
    async likeImage(item) {
      const data = JSON.stringify({
        date: item.date,
        email: this.getEmail,
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
        .catch((error) => {
          this.$store.commit("addErrorMessage", "Failed to like the image");
        });
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
        .catch((error) => {
          this.$store.commit("addErrorMessage", "Failed to remove the like from the image");
        });
    },
    selectAndShowModal(item) {
      this.$emit("selectedItem", item);
      const modal = document.getElementById("exampleModal");
      if (modal) {
        const modalInstance = bootstrap.Modal.getInstance(modal) || new bootstrap.Modal(modal);
        modalInstance.show();
      }
    },
  },
};
</script>

<style scoped>
.image-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  width: 100%;
}

.image-container:hover {
  display: block;
}

.image-container:focus {
  outline: 2px solid blue;
}

.like-icon-container {
  padding: 0.5rem 1rem 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
}

.like-icon-container:hover {
  background-color: #f0f0f0;
}

.custom-small-text {
  margin: 0px;
}

.marquee-container {
  overflow: hidden;
}

.marquee-container p {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
</style>
