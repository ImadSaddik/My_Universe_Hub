import { test, expect, type Page } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test.describe("Acknowledgement Bar", () => {
  test("should display the APOD link correctly", async ({ page }) => {
    const apodLink = page.getByTestId("apod-link");

    await expect(apodLink).toBeVisible();
    await expect(apodLink).toHaveText("APOD");
    await expect(apodLink).toHaveAttribute("href", "https://apod.nasa.gov/");
    await expect(apodLink).toHaveAttribute("target", "_blank");
    await expect(apodLink).toHaveAttribute("rel", "noopener noreferrer");
  });

  test("should contain the full acknowledgement text from fixture", async ({ page }) => {
    const acknowledgementText = page.getByTestId("acknowledgement-text");
    await expect(acknowledgementText).toContainText(
      "This website is a redesign of the Astronomy Picture of the Day (APOD). Images are credited to their respective astrophotographers. For more details, visit"
    );
  });
});
