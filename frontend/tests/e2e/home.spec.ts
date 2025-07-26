import { test, expect } from "@playwright/test";

const searchSectionData = {
  title: "My Universe Hub",
  description: "Discover images by entering keywords separated by commas. Find the image you are looking for.",
  placeholder: "Andromeda, Jupiter, Pluto, M31",
};

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test.describe("Home page", () => {
  test("should display the correct title", async ({ page }) => {
    await expect(page).toHaveTitle("Home");
  });

  test.describe("Hero section", () => {
    test("displays all hero section elements correctly", async ({ page }) => {
      // Title
      const heroTitle = page.getByTestId("hero-title");
      await expect(heroTitle).toBeVisible();
      await expect(heroTitle).toHaveText(searchSectionData.title);

      // Description
      const heroDescription = page.getByTestId("hero-description");
      await expect(heroDescription).toBeVisible();
      await expect(heroDescription).toHaveText(searchSectionData.description);

      // Search input
      const searchInput = page.getByTestId("search-input");
      await expect(searchInput).toBeVisible();
      await expect(searchInput).toHaveValue("");
      await expect(searchInput).toHaveAttribute("placeholder", searchSectionData.placeholder);

      // Background image
      const backgroundImage = page.getByTestId("background-image");
      await expect(backgroundImage).toBeVisible();
      await expect(backgroundImage).toHaveAttribute("src", /search_background\.jpg/);
    });
  });

  test.describe("Load more button", () => {
    test("Should load more items when clicked", async ({ page }) => {
      // Check if load more button is visible
      const loadMoreButton = page.getByTestId("load-more-button");
      await expect(loadMoreButton).toBeVisible();
      await expect(loadMoreButton).toHaveText("Load more");

      // Check number of gallery items
      let galleryItems = page.getByTestId("gallery-item");
      await expect(galleryItems).toHaveCount(10);

      // Load more items
      await loadMoreButton.click();
      galleryItems = page.getByTestId("gallery-item");
      await expect(galleryItems).toHaveCount(20);
    });
  });

  test.describe("Scroll to top button", () => {
    test("scroll to top button behavior", async ({ page }) => {
      // Initially not visible
      let scrollToTopButton = page.getByTestId("scroll-to-top-button");
      await expect(scrollToTopButton).toHaveAttribute("src", /circle-arrow-up-solid\.svg/);
      await expect(scrollToTopButton).not.toBeVisible();

      // Check number of gallery items
      let galleryItems = page.getByTestId("gallery-item");
      await expect(galleryItems).toHaveCount(10);

      // Load more items
      const loadMoreButton = page.getByTestId("load-more-button");
      await expect(loadMoreButton).toBeVisible();
      await loadMoreButton.click();

      galleryItems = page.getByTestId("gallery-item");
      await expect(galleryItems).toHaveCount(20);

      // Scroll down
      const scrollDownAmount = 800;
      await page.mouse.wheel(0, scrollDownAmount);

      scrollToTopButton = page.getByTestId("scroll-to-top-button");
      await expect(scrollToTopButton).toBeVisible();
      await scrollToTopButton.click();

      // Scroll back to top
      await page.mouse.wheel(0, 0);
      await expect(scrollToTopButton).not.toBeVisible();
    });
  });

  test.describe("Gallery", () => {
    test("displays gallery when data is available", async ({ page }) => {
      const galleryItems = page.getByTestId("gallery-item");
      await expect(galleryItems).toHaveCount(10);

      const count = await galleryItems.count();
      for (let i = 0; i < count; i++) {
        const item = galleryItems.nth(i);
        await expect(item).toBeVisible();

        const image = item.getByTestId("gallery-item-image");
        await expect(image).toBeVisible();
        expect(await image.getAttribute("src")).not.toBeNull();

        const appLogo = item.getByTestId("gallery-item-app-logo");
        await expect(appLogo).toBeVisible();
        await expect(appLogo).toHaveAttribute("src", /galaxy_logo\.svg/);

        const title = item.getByTestId("gallery-item-title");
        await expect(title).toBeVisible();

        const titleText = await title.textContent();
        expect(titleText).not.toBeNull();
        expect(titleText?.trim()).not.toBe("");

        const heartAndCountContainer = item.getByTestId("gallery-item-action");
        await expect(heartAndCountContainer).toBeVisible();

        const heartIcon = heartAndCountContainer.locator("i.fa-heart");
        await expect(heartIcon).toBeVisible();

        const likeUnlikeContainer = item.getByTestId("gallery-item-unlike-or-like");
        const likeUnlikeText = await likeUnlikeContainer.textContent();
        expect(likeUnlikeText).toMatch(/\d+/);

        const imageCredit = item.getByTestId("gallery-item-image-credit");
        await expect(imageCredit).toBeVisible();
        await expect(imageCredit).toHaveText(/Image credit:/);

        const postedDate = item.getByTestId("gallery-item-date");
        await expect(postedDate).toBeVisible();

        const postedDateParent = postedDate.locator("..");
        await expect(postedDateParent).toContainText("Posted:");
        await expect(postedDateParent).toContainText("on");

        const apodLink = item.getByTestId("gallery-item-apod-link");
        await expect(apodLink).toBeVisible();
        await expect(apodLink).toHaveText("APOD");
        await expect(apodLink).toHaveAttribute("href", "https://apod.nasa.gov/");
        await expect(apodLink).toHaveAttribute("target", "_blank");
      }
    });

    test("should show the modal with image details and correct structure when an item is clicked", async ({ page }) => {
      const galleryItems = page.getByTestId("gallery-item");
      await expect(galleryItems).toHaveCount(10);
      await page.waitForTimeout(3000);

      const firstItem = galleryItems.nth(0);
      await expect(firstItem).toBeVisible();
      await firstItem.click();

      const modal = page.getByTestId("image-details-modal");
      await expect(modal).toBeVisible();

      const appLogo = modal.getByTestId("modal-app-logo");
      await expect(appLogo).toBeVisible();
      await expect(appLogo).toHaveAttribute("src", /galaxy_logo\.svg/);

      const modalHeartContainer = modal.getByTestId("modal-heart-and-count-container");
      await expect(modalHeartContainer).toBeVisible();

      const heartIcon = modalHeartContainer.locator("i.fa-heart");
      await expect(heartIcon).toBeVisible();

      const likeCountContainer = modal.getByTestId("modal-like-count-text-container");
      const likeUnlikeText = await likeCountContainer.textContent();
      expect(likeUnlikeText).toMatch(/\d+/);

      const downloadIcon = modal.getByTestId("modal-download-icon");
      await expect(downloadIcon).toBeVisible();

      const closeModalIcon = modal.getByTestId("modal-close-icon");
      await expect(closeModalIcon).toBeVisible();

      const modalBody = modal.getByTestId("modal-body");
      await expect(modalBody).toBeVisible();

      const image = modalBody.getByTestId("modal-image");
      await expect(image).toBeVisible();
      expect(await image.getAttribute("src")).not.toBeNull();

      const title = modalBody.getByTestId("modal-title");
      await expect(title).toBeVisible();

      const titleText = await title.textContent();
      expect(titleText).not.toBeNull();
      expect(titleText?.trim()).not.toBe("");

      const imageCredit = modalBody.getByTestId("modal-image-credit");
      await imageCredit.scrollIntoViewIfNeeded();
      await expect(imageCredit).toBeVisible();
      await expect(imageCredit).toHaveText(/Image credit:/);

      const postedDate = modalBody.getByTestId("modal-posted-date");
      await expect(postedDate).toBeVisible();

      const explanation = modalBody.getByTestId("modal-explanation");
      await explanation.scrollIntoViewIfNeeded();
      await expect(explanation).toBeVisible();
      await expect(explanation).toHaveText(/Explanation:/);

      const postedDateParent = postedDate.locator("..");
      await expect(postedDateParent).toContainText("Posted:");
      await expect(postedDateParent).toContainText("on");

      const apodLink = modalBody.getByTestId("modal-apod-link");
      await apodLink.scrollIntoViewIfNeeded();
      await expect(apodLink).toBeVisible();
      await expect(apodLink).toHaveText("APOD");
      await expect(apodLink).toHaveAttribute("href", "https://apod.nasa.gov/");
      await expect(apodLink).toHaveAttribute("target", "_blank");

      await closeModalIcon.click();
      await expect(modal).not.toBeVisible();
    });
  });

  test.describe("Search functionality", () => {
    test("should display search results when a query is entered", async ({ page }) => {
      const searchInput = page.getByTestId("search-input");
      await expect(searchInput).toBeVisible();
      await expect(searchInput).toHaveValue("");

      const searchQuery = "Andromeda";
      await searchInput.fill(searchQuery);
      await searchInput.press("Enter");

      const galleryItems = page.getByTestId("gallery-item");
      await expect(galleryItems).toHaveCount(10);

      const noResultsMessage = page.getByTestId("no-results-message");
      await expect(noResultsMessage).not.toBeVisible();
    });

    test("should show no results for keywords that do not match anything", async ({ page }) => {
      const searchInput = page.getByTestId("search-input");
      await expect(searchInput).toBeVisible();
      await expect(searchInput).toHaveValue("");

      const searchQuery = "xx";
      await searchInput.fill(searchQuery);
      await searchInput.press("Enter");

      const galleryItems = page.getByTestId("gallery-item");
      await expect(galleryItems).toHaveCount(0);

      const noResultsMessage = page.getByTestId("no-results-message");
      await expect(noResultsMessage).toBeVisible();
    });
  });
});
