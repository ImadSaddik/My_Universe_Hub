<template>
  <div class="container pt-2 pt-sm-5">
    <div v-if="!error">
      <div v-if="isTodayEntryAvailable">
        <div class="row m-0 my-3 d-flex flex-column">
          <div class="col d-flex justify-content-center">
            <h1 class="custom-title-text">{{ data.title }}</h1>
          </div>
          <div
            v-if="Object.keys(data).length"
            class="mt-2 col d-flex justify-content-center"
          >
            <div v-if="isLoggedIn">
              <div
                v-if="data.image_is_liked"
                class="like-icon-container d-flex align-items-center"
                @click="unlikeImage(data)"
              >
                {{ data.image_likes_count }}
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
                @click="likeImage(data)"
              >
                {{ data.image_likes_count }}
                <i type="button" class="ms-2 fa-regular fa-heart fa-xl"> </i>
              </div>
            </div>
            <div v-else>
              <div class="like-icon-container d-flex align-items-center">
                {{ data.image_likes_count }}
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
        <div class="row m-0 mt-4 mt-sm-5">
          <div class="col d-flex justify-content-center">
            <img
              type="button"
              :src="data.image_url"
              class="img-fluid rounded-4"
              alt=""
              @click="downloadImage"
            />
          </div>
        </div>
        <div class="row m-0 mt-4 mt-sm-5">
          <div class="col d-flex justify-content-center">
            <p class="custom-small-text">
              <b>Image credit:</b> {{ data.authors }}
            </p>
            <p class="custom-small-text ms-3">
              <b>Posted:</b> {{ data.date }} on
              <a
                href="https://apod.nasa.gov/"
                target="_blank"
                rel="noopener noreferrer"
                >APOD</a
              >
            </p>
          </div>
        </div>
        <div class="row m-0 mt-3 mt-sm-4 mb-3">
          <div class="col px-sm-3">
            <p
              class="custom-small-text"
              v-html="formatExplanation(data.explanation)"
            ></p>
          </div>
        </div>
      </div>
      <div
        v-else
        class="row d-flex align-items-center justify-content-center"
        style="height: calc(80vh)"
      >
        <h5 class="nav-link text-center">
          Trying to fetch data from source, be patient
          <i class="ms-2 fa-solid fa-hurricane fa-spin"></i>
        </h5>
      </div>
    </div>
    <div
      v-else
      class="row d-flex align-items-center justify-content-center"
      style="height: calc(80vh)"
    >
      <h5 class="nav-link text-center">
        No image for today 😔, see you tomorrow.
      </h5>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TodayPictureView",
  components: {},
  computed: {
    isLoggedIn() {
      return this.$store.state.token !== "";
    },
    getEmail() {
      return this.$store.state.email;
    },
    isTodayEntryAvailable() {
      if (this.data === null) {
        return false;
      } else {
        if (this.data.image_url === null) {
          return false;
        } else {
          return true;
        }
      }
    },
  },
  data() {
    return {
      data: null,
      error: null,
    };
  },
  async mounted() {
    document.title = "Today's Picture";
    await this.getTodayPicture();
  },
  methods: {
    async getTodayPicture() {
      await axios
        .get("/api/v1/today/")
        .then((response) => {
          const email = this.getEmail;
          this.data = response.data;

          if (email) {
            this.data.image_is_liked =
              response.data.liked_by_users.includes(email);
          }
        })
        .catch((error) => {
          this.error = error;
        });
    },
    downloadImage() {
      const imageUrl = this.data.image_url;
      const anchorTag = document.createElement("a");
      anchorTag.href = imageUrl;
      anchorTag.target = "_blank";

      document.body.appendChild(anchorTag);
      anchorTag.click();
      document.body.removeChild(anchorTag);
    },
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

<style scoped>
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
</style>
