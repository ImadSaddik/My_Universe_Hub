import pluginVue from "eslint-plugin-vue";
import globals from "globals";

export default [
  ...pluginVue.configs["flat/recommended"],
  ...pluginVue.configs["flat/strongly-recommended"],
  {
    rules: {
      "vue/no-unused-vars": "error",
    },
    languageOptions: {
      sourceType: "module",
      globals: {
        ...globals.browser,
      },
    },
  },
];
