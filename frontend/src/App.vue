<template>
  <NavBar/>
  <router-view/>
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: {
    NavBar
  }
}
</script>

<style>
.custom-btn {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px !important;
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
  color: #333;
  border-color: #333;
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
  content: '';
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
  0% {
    transform: scale(0, 0);
    opacity: 1;
  }
  20% {
    transform: scale(150, 150);
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: scale(150, 150);
  }
}

.custom-btn:focus:not(:active)::after {
  animation: ripple 1s ease-out;
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
  border-radius: 5px;
  font-size: 1rem;
}

.input-field:focus {
  border-color: #007bff;
  outline: none;
}

.toggle-password-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #aaa;
}

.toggle-password-icon:hover {
  color: black;
  cursor: pointer;
}

.outer-card-container {
  padding: 2rem;
  border-radius: 1rem;
  background-color: rgba(255, 255, 255, .1);
  color: white;
}

@media (max-width: 576px) {
  .input-field {
    padding: 0.5rem 0.5rem 0.5rem 2rem;
  }
  .input-icon {
    left: 0.5rem;
  }
}
</style>
