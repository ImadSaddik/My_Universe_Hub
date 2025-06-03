import { defineConfig } from "cypress";
import dotenv from "dotenv";

dotenv.config();

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:8080",
    viewportWidth: 1280,
    viewportHeight: 1280,
    defaultCommandTimeout: 15000,
    requestTimeout: 15000,
    responseTimeout: 15000,
    setupNodeEvents(on, config) {
      config.env.TEST_USER_EMAIL = process.env.TEST_USER_EMAIL;
      config.env.TEST_USER_PASSWORD = process.env.TEST_USER_PASSWORD;
      return config;
    },
  },
});
