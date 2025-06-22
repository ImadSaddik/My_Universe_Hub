import { test, expect, type Page } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test.describe("Login Feature", () => {
  test("should login successfully and redirect to home", async ({ page }) => {
    // Wait for initial page load
    await expect(page).toHaveTitle("Home");

    // Navigate to login
    const loginNavLink = page.getByTestId("nav-link-login");
    await expect(loginNavLink).toBeVisible();
    await loginNavLink.click();

    // Wait for login page to load
    await expect(page).toHaveTitle("Log In");

    // Fill credentials
    const emailInput = page.getByTestId("login-email");
    const passwordInput = page.getByTestId("login-password");

    await expect(emailInput).toBeVisible();
    await expect(passwordInput).toBeVisible();

    const email = process.env.TEST_USER_EMAIL;
    const password = process.env.TEST_USER_PASSWORD;

    if (!email || !password) {
      throw new Error("TEST_USER_EMAIL and TEST_USER_PASSWORD must be set");
    }

    await emailInput.fill(email);
    await passwordInput.fill(password);

    // Submit and wait for navigation
    const submitButton = page.getByTestId("login-submit");
    await expect(submitButton).toBeVisible();
    await expect(submitButton).toBeEnabled();

    await submitButton.click();

    // Wait for successful redirect
    await expect(page).toHaveURL("/");
    await expect(page).toHaveTitle("Home");
  });
});
