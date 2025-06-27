<template>
  <div class="error-notifications-container">
    <div
      v-for="error in errorMessages"
      :key="error.id"
      class="error-notification"
      @mouseenter="pauseTimer(error.id)"
      @mouseleave="resumeTimer(error.id)"
    >
      <span>{{ error.message }}</span>
      <i
        class="fa-solid fa-xmark fa-2xl p-2 p-sm-2 close-button"
        role="button"
        tabindex="0"
        aria-label="Close notification"
        @keydown.enter="closeNotification(error.id)"
        @click="closeNotification(error.id)"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "ErrorNotification",
  data() {
    return {
      timers: new Map(),
    };
  },
  computed: {
    errorMessages() {
      return this.$store.state.errorMessages;
    },
  },
  watch: {
    errorMessages: {
      handler(newErrors, oldErrors) {
        const addedErrors = newErrors.filter((newError) => !oldErrors.find((oldError) => oldError.id === newError.id));
        addedErrors.forEach((newError) => this.startTimer(newError.id));

        const removedErrors = oldErrors.filter(
          (oldError) => !newErrors.find((newError) => newError.id === oldError.id)
        );
        removedErrors.forEach((newError) => this.clearTimer(newError.id));
      },
      deep: true,
    },
  },
  mounted() {
    this.errorMessages.forEach((error) => this.startTimer(error.id));
  },
  beforeUnmount() {
    this.timers.forEach((timer) => clearTimeout(timer));
  },
  methods: {
    removeErrorMessage(errorId) {
      this.$store.commit("removeErrorMessage", errorId);
    },
    startTimer(errorId) {
      if (this.timers.has(errorId)) return;
      const timer = setTimeout(() => {
        this.removeErrorMessage(errorId);
      }, 5000);
      this.timers.set(errorId, timer);
    },
    clearTimer(errorId) {
      if (this.timers.has(errorId)) {
        clearTimeout(this.timers.get(errorId));
        this.timers.delete(errorId);
      }
    },
    pauseTimer(errorId) {
      if (this.timers.has(errorId)) {
        clearTimeout(this.timers.get(errorId));
      }
    },
    resumeTimer(errorId) {
      this.timers.delete(errorId);
      this.startTimer(errorId);
    },
    closeNotification(errorId) {
      this.clearTimer(errorId);
      this.removeErrorMessage(errorId);
    },
  },
};
</script>

<style scoped>
.error-notifications-container {
  position: fixed;
  bottom: 1.5rem;
  left: 1.5rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.error-notification {
  background-color: #98242f;
  color: white;
  padding: 1rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  width: 500px;
}

@media (max-width: 600px) {
  .error-notification {
    width: 100%;
  }

  .error-notifications-container {
    left: 1rem;
    right: 1rem;
  }
}

.close-button:focus {
  outline: 2px solid white;
}

.close-button:hover {
  color: #b5b5b5;
}
</style>
