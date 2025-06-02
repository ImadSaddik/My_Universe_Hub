import { defineConfig } from "cypress";
import dotenv from "dotenv";

dotenv.config();

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:8080",
    viewportWidth: 1280,
    viewportHeight: 1280,
    setupNodeEvents(on, config) {
      config.env.TEST_LOGIN_EMAIL = process.env.TEST_LOGIN_EMAIL;
      config.env.TEST_LOGIN_PASSWORD = process.env.TEST_LOGIN_PASSWORD;
      return config;
    },
  },
});
