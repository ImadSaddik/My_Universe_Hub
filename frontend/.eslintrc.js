module.exports = {
  env: {
    node: true,
    browser: true,
    es2022: true,
  },
  extends: ["eslint:recommended", "plugin:vue/recommended"],
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: "module",
  },
  rules: {
    quotes: "error",
  },
};
