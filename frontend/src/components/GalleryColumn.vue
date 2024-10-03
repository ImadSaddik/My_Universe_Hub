<template>
  <div class="col-12 col-sm-6 col-lg-4 py-0">
    <div v-for="(item, index) in archive" :key="index" class="mb-3">
      <div>
        <img
          :src="item.image_url"
          v-lazy="item.image_url"
          class="img-fluid image-container"
          alt=""
          @click="$emit('selectedItem', item)"
          data-bs-toggle="modal"
          data-bs-target="#exampleModal"
        />
        <div class="row m-0">
          <div class="col py-1 d-flex align-items-center marquee-container">
            <img
              src="../assets/logos/galaxy_logo.svg"
              alt=""
              style="width: 2rem"
            />
            <p class="custom-small-text m-0 ms-3 fw-bold">{{ item.title }}</p>
          </div>
          <div class="col-auto p-0 py-1">
            <div v-if="isLoggedIn">
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
            <div v-else>
              <div
                class="like-icon-container d-flex align-items-center"
              >
                {{ item.image_likes_count }}
                <i
                  :disabled="!isLoggedIn"
                  class="ms-2 fa-regular fa-heart fa-xl"
                  style="color: #77767b"
                >
                </i>
              </div>
            </div>
          </div>
        </div>
        <div>
          <p class="custom-small-text">
            <b>Image credit:</b> {{ item.authors }}
          </p>
          <p class="custom-small-text">
            <b>Posted:</b> {{ item.date }} on
            <a
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
  props: ["archive"],
  components: {},
  computed: {
    isLoggedIn() {
      return this.$store.state.token !== "";
    },
    getEmail() {
      return this.$store.state.email;
    },
  },
  data() {
    return {
      selectedItem: null,
    };
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
        .catch((error) => {});
    },
    async unlikeImage(item) {
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

.like-icon-container {
  padding: 0.5rem 1rem 0.5rem 1rem;
  /* border: 1px solid #ccc; */
  border-radius: 0.5rem;
  cursor: pointer;
}

.like-icon-container:hover {
  background-color: #f0f0f0;
  /* border: 1px solid #aaa; */
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
