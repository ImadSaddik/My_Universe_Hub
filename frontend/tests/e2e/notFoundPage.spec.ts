import { test, expect, type Page } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.goto("/Oops-404");
});

test.describe("404 Not found page", () => {
  test("should display the correct title", async ({ page }) => {
    await expect(page).toHaveTitle("404 - Page not found | MyUniverseHub");
  });

  test("should display all 404 page elements correctly", async ({ page }) => {
    // Check heading
    const heading = page.getByTestId("error-heading");
    await expect(heading).toBeVisible();
    await expect(heading).toHaveText("404 - Page not found");

    // Check error message
    const errorMessage = page.getByTestId("error-message");
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText("Sorry, the page you are looking for does not exist.");

    // Check "Return to Home" link
    const homeLink = errorMessage.getByRole("link", { name: "Return to Home" });
    await expect(homeLink).toBeVisible();
    await expect(homeLink).toHaveAttribute("href", "/");

    // Check stars and galaxies image
    const starsImage = page.getByTestId("stars-and-galaxies-image");
    await expect(starsImage).toBeVisible();
    await expect(starsImage).toHaveAttribute("src", /stars_and_galaxies\.svg/);
    await expect(starsImage).toHaveAttribute("aria-hidden", "true");

    // Check telescope image
    const telescopeImage = page.getByTestId("telescope-image");
    await expect(telescopeImage).toBeVisible();
    await expect(telescopeImage).toHaveAttribute("src", /telescope\.svg/);
    await expect(telescopeImage).toHaveAttribute("aria-hidden", "true");
  });

  test("should navigate back to home when clicking 'Return to Home' link", async ({ page }) => {
    const homeLink = page.getByRole("link", { name: "Return to Home" });
    await homeLink.click();

    await expect(page).toHaveURL("/");
    await expect(page).toHaveTitle("Home");
  });

  test("should clear navbar selection state", async ({ page }) => {
    // All navigation links should have normal font weight (not bold)
    const navLinks = [
      page.getByTestId("nav-link-home"),
      page.getByTestId("nav-link-today"),
      page.getByTestId("nav-link-trending"),
      page.getByTestId("nav-link-favourites"),
      page.getByTestId("nav-link-about"),
      page.getByTestId("nav-link-contribute"),
    ];

    for (const link of navLinks) {
      await expect(link).toHaveCSS("font-weight", "400");
    }
  });

  test("should hide telescope image on mobile viewport", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });

    const telescopeImage = page.getByTestId("telescope-image");
    await expect(telescopeImage).not.toBeVisible();

    const starsImage = page.getByTestId("stars-and-galaxies-image");
    await expect(starsImage).toBeVisible();
  });

  test("should show telescope image on desktop viewport", async ({ page }) => {
    await page.setViewportSize({ width: 1024, height: 768 });

    const telescopeImage = page.getByTestId("telescope-image");
    await expect(telescopeImage).toBeVisible();

    const starsImage = page.getByTestId("stars-and-galaxies-image");
    await expect(starsImage).toBeVisible();
  });
});
