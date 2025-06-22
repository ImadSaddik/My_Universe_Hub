import { test, expect } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test.describe("Home Page", () => {
  test("should display the correct title", async ({ page }) => {
    await expect(page).toHaveTitle("Home");
  });

  test.describe("Navigation bar", () => {
    test("shows the logo in the navigation bar", async ({ page }) => {
      const logo = page.getByTestId("nav-link-app-logo");
      await expect(logo).toBeVisible();
    });

    test("should show the 'home' text in bold in the navigation bar", async ({ page }) => {
      // Check that Home is bold (font-weight 700)
      const homeLink = page.getByTestId("nav-link-home");
      await expect(homeLink).toHaveCSS("font-weight", "700");

      // Check that all other links are not bold (font-weight 400)
      const otherLinks = [
        page.getByTestId("nav-link-today"),
        page.getByTestId("nav-link-trending"),
        page.getByTestId("nav-link-favourites"),
        page.getByTestId("nav-link-contribute"),
        page.getByTestId("nav-link-about"),
      ];

      for (const link of otherLinks) {
        await expect(link).toHaveCSS("font-weight", "400");
      }
    });

    test("should show all navigation links", async ({ page }) => {
      const navLinks = [
        page.getByTestId("nav-link-home"),
        page.getByTestId("nav-link-today"),
        page.getByTestId("nav-link-trending"),
        page.getByTestId("nav-link-favourites"),
        page.getByTestId("nav-link-contribute"),
        page.getByTestId("nav-link-about"),
      ];

      for (const link of navLinks) {
        await expect(link).toBeVisible();
      }
    });

    test("shows the GitHub link", async ({ page }) => {
      const githubLink = page.getByTestId("github-link");
      const starCount = page.getByTestId("github-star-count");

      await expect(githubLink).toBeVisible();
      await expect(starCount).toBeVisible();
    });

    test("shows the log in button", async ({ page }) => {
      const loginButton = page.getByTestId("nav-link-login");
      const logoutButton = page.getByTestId("nav-link-logout");

      await expect(loginButton).toBeVisible();
      await expect(loginButton).toContainText("Log In");
      await expect(logoutButton).not.toBeVisible();
    });

    test("shows the correct tooltip on hovering the login button", async ({ page }) => {
      const loginButton = page.getByTestId("nav-link-login");

      await loginButton.hover();
      const tooltip = page.locator("div.tooltip-inner");
      await expect(tooltip).toBeVisible();
      await expect(tooltip).toHaveText("Log In");

      // Move mouse away to hide tooltip
      await page.mouse.move(0, 0);
      await expect(tooltip).not.toBeVisible();
    });

    test("shows the correct tooltip on hovering the GitHub link", async ({ page }) => {
      const githubLink = page.getByTestId("github-link");

      await githubLink.hover();
      const tooltip = page.locator("div.tooltip-inner");
      await expect(tooltip).toBeVisible();
      await expect(tooltip).toHaveText("GitHub repository");

      // Move mouse away to hide tooltip
      await page.mouse.move(0, 0);
      await expect(tooltip).not.toBeVisible();
    });

    test("checks all hrefs in the navigation bar", async ({ page }) => {
      const linkTests = [
        { testId: "nav-link-home", expectedHref: "/" },
        { testId: "nav-link-today", expectedHref: "/today" },
        { testId: "nav-link-trending", expectedHref: "/trending" },
        { testId: "nav-link-favourites", expectedHref: "/favourites" },
        { testId: "nav-link-about", expectedHref: "/about" },
        { testId: "nav-link-contribute", expectedHref: "/contribute" },
        { testId: "nav-link-login", expectedHref: "/login" },
        { testId: "github-link", expectedHref: /github\.com/ },
      ];

      for (const { testId, expectedHref } of linkTests) {
        await expect(page.getByTestId(testId)).toHaveAttribute("href", expectedHref);
      }
    });
  });

  test.describe("Clicking navigation links", () => {
    test("should navigate to the 'Today' page", async ({ page }) => {
      await page.getByTestId("nav-link-today").click();

      await expect(page).toHaveURL(/\/today/);
      await expect(page).toHaveTitle("Today's Picture");

      // Check active state
      await expect(page.getByTestId("nav-link-today")).toHaveCSS("font-weight", "700");

      const otherLinks = [
        page.getByTestId("nav-link-home"),
        page.getByTestId("nav-link-trending"),
        page.getByTestId("nav-link-favourites"),
        page.getByTestId("nav-link-about"),
        page.getByTestId("nav-link-contribute"),
      ];

      for (const link of otherLinks) {
        await expect(link).toHaveCSS("font-weight", "400");
      }
    });

    test("should navigate to the 'Trending' page", async ({ page }) => {
      await page.getByTestId("nav-link-trending").click();

      await expect(page).toHaveURL(/\/trending/);
      await expect(page).toHaveTitle("Trending");

      // Check active state
      await expect(page.getByTestId("nav-link-trending")).toHaveCSS("font-weight", "700");

      const otherLinks = [
        page.getByTestId("nav-link-home"),
        page.getByTestId("nav-link-today"),
        page.getByTestId("nav-link-favourites"),
        page.getByTestId("nav-link-about"),
        page.getByTestId("nav-link-contribute"),
      ];

      for (const link of otherLinks) {
        await expect(link).toHaveCSS("font-weight", "400");
      }
    });

    test("should navigate to the 'Favourites' page", async ({ page }) => {
      await page.getByTestId("nav-link-favourites").click();

      await expect(page).toHaveURL(/\/favourites/);
      await expect(page).toHaveTitle("Favourites");

      // Check active state
      await expect(page.getByTestId("nav-link-favourites")).toHaveCSS("font-weight", "700");

      const otherLinks = [
        page.getByTestId("nav-link-home"),
        page.getByTestId("nav-link-today"),
        page.getByTestId("nav-link-trending"),
        page.getByTestId("nav-link-about"),
        page.getByTestId("nav-link-contribute"),
      ];

      for (const link of otherLinks) {
        await expect(link).toHaveCSS("font-weight", "400");
      }
    });

    test("should navigate to the 'Contribute' page", async ({ page }) => {
      await page.getByTestId("nav-link-contribute").click();

      await expect(page).toHaveURL(/\/contribute/);
      await expect(page).toHaveTitle("Contribute");

      // Check active state
      await expect(page.getByTestId("nav-link-contribute")).toHaveCSS("font-weight", "700");

      const otherLinks = [
        page.getByTestId("nav-link-home"),
        page.getByTestId("nav-link-today"),
        page.getByTestId("nav-link-trending"),
        page.getByTestId("nav-link-favourites"),
        page.getByTestId("nav-link-about"),
      ];

      for (const link of otherLinks) {
        await expect(link).toHaveCSS("font-weight", "400");
      }
    });

    test("should navigate to the 'About' page", async ({ page }) => {
      await page.getByTestId("nav-link-about").click();

      await expect(page).toHaveURL(/\/about/);
      await expect(page).toHaveTitle("About");

      // Check active state
      await expect(page.getByTestId("nav-link-about")).toHaveCSS("font-weight", "700");

      const otherLinks = [
        page.getByTestId("nav-link-home"),
        page.getByTestId("nav-link-today"),
        page.getByTestId("nav-link-trending"),
        page.getByTestId("nav-link-favourites"),
        page.getByTestId("nav-link-contribute"),
      ];

      for (const link of otherLinks) {
        await expect(link).toHaveCSS("font-weight", "400");
      }
    });

    test("should navigate to the 'Home' page after clicking the logo", async ({ page }) => {
      // First navigate away from home
      await page.getByTestId("nav-link-today").click();
      await expect(page).toHaveURL(/\/today/);

      // Then click logo to go back to home
      await page.getByTestId("nav-link-app-logo").click();

      await expect(page).toHaveURL("/");
      await expect(page).toHaveTitle("Home");

      // Check active state
      await expect(page.getByTestId("nav-link-home")).toHaveCSS("font-weight", "700");

      const otherLinks = [
        page.getByTestId("nav-link-today"),
        page.getByTestId("nav-link-trending"),
        page.getByTestId("nav-link-favourites"),
        page.getByTestId("nav-link-about"),
        page.getByTestId("nav-link-contribute"),
      ];

      for (const link of otherLinks) {
        await expect(link).toHaveCSS("font-weight", "400");
      }
    });

    test("should navigate to the 'Login' page", async ({ page }) => {
      await page.getByTestId("nav-link-login").click();

      await expect(page).toHaveURL(/\/login/);
      await expect(page).toHaveTitle("Log In");

      // On login page, no nav links should be bold
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
  });
});
