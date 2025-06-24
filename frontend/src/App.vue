<template>
  <NavBar />
  <AcknowledgementBar />
  <router-view />
  <ErrorNotification />
</template>

<script>
import NavBar from "./components/NavBar.vue";
import AcknowledgementBar from "./components/AcknowledgementBar.vue";
import ErrorNotification from "./components/ErrorNotification.vue";

export default {
  name: "App",
  components: {
    NavBar,
    AcknowledgementBar,
    ErrorNotification,
  },
};
</script>

<style>
a {
  color: blue;
  text-decoration: underline;
}

.custom-small-text {
  font-size: 1rem;
  line-height: 1.75;
}

.custom-title-text {
  font-size: 2rem;
  font-weight: bold;
}

.custom-subtitle-text {
  font-size: 1.5rem;
  font-weight: bold;
}

/*  */

.custom-btn {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem !important;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  width: 100%;
}

.custom-btn-white {
  background-color: white;
  color: black;
}

.custom-btn-white:hover {
  background-color: #f0f0f0;
  border-color: #aaa !important;
}

.custom-btn-black {
  background-color: black;
  color: white;
}

.custom-btn-black:hover {
  background-color: #333;
  color: #f0f0f0;
  border-color: #f0f0f0;
}

.custom-btn::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(0, 0, 0, 0.3);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%, -50%);
  transform-origin: 50% 50%;
}

@keyframes ripple {
  from {
    opacity: 1;
    transform: scale(0);
  }

  to {
    opacity: 0;
    transform: scale(1000);
  }
}

.custom-btn:focus:not(:active)::after {
  animation: ripple 0.5s ease-out;
}

/*  */

.input-container {
  position: relative;
  margin-bottom: 1rem;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #aaa;
}

.input-field {
  width: 100%;
  padding: 1rem 1rem 1rem 2.5rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.input-field:focus {
  outline: 2px solid blue;
}

.toggle-password-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #aaa;
  font-size: 1.25rem;
  padding: 0.5rem;
}

.toggle-password-icon:hover {
  color: black;
  cursor: pointer;
}

@media (max-width: 576px) {
  .custom-small-text {
    font-size: 0.75rem;
    line-height: 1.5;
  }
}
</style>
