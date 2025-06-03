describe("Home Page", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("should display the correct title", () => {
    cy.title().should("eq", "Home");
  });

  describe("Hero section", () => {
    it("checks the title", () => {
      cy.get('[data-cy="hero-title"]').should("be.visible");
      cy.fixture("searchSection.json").then((data) => {
        cy.get('[data-cy="hero-title"]').contains(data.title);
      });
    });

    it("checks the description", () => {
      cy.get('[data-cy="hero-description"]').should("be.visible");
      cy.fixture("searchSection.json").then((data) => {
        cy.get('[data-cy="hero-description"]').contains(data.description);
      });
    });

    it("should show a search input", () => {
      cy.get('[data-cy="search-input"]').should("be.visible");
      cy.get('[data-cy="search-input"]').should("have.value", "");
      cy.get('[data-cy="search-input"]').should("have.attr", "placeholder", "Andromeda, Jupiter, Pluto, M31");
    });

    it("shows a background image", () => {
      cy.get('[data-cy="background-image"]').should("be.visible");
      cy.get('[data-cy="background-image"]').should("have.attr", "src").and("include", "search_background.jpg");
    });
  });

  describe("Scroll to top button", () => {
    const scrollDownAmount = 600;

    it("should not be visible initially", () => {
      cy.get('[data-cy="scroll-to-top-button"]').should("not.be.visible");
    });

    it("should be visible when scrolled down", () => {
      cy.get('[data-cy="load-more-button"]').click();
      cy.wait(1000);
      cy.scrollTo(0, scrollDownAmount);
      cy.get('[data-cy="scroll-to-top-button"]').should("be.visible");
    });

    it("should scroll to top when clicked", () => {
      cy.get('[data-cy="load-more-button"]').click();
      cy.wait(1000);
      cy.scrollTo(0, scrollDownAmount);
      cy.get('[data-cy="scroll-to-top-button"]').click();
      cy.window().its("scrollY").should("equal", 0);
      cy.get('[data-cy="scroll-to-top-button"]').should("not.be.visible");
    });

    it("should show the correct icon", () => {
      cy.get('[data-cy="scroll-to-top-button"]').should("have.attr", "src").and("include", "circle-arrow-up-solid.svg");
    });
  });

  describe("Load more button", () => {
    it("should display the 'Load more' button", () => {
      cy.get('[data-cy="load-more-button"]').should("be.visible");
      cy.get('[data-cy="load-more-button"]').should("contain.text", "Load more");
    });

    it("should load more items when clicked", () => {
      cy.get('[data-cy="gallery-item"]').should("have.length", 10);
      cy.get('[data-cy="load-more-button"]').click();
      cy.get('[data-cy="gallery-item"]').should("have.length", 20);
    });
  });

  describe("Gallery items", () => {
    it("should display gallery items", () => {
      cy.get('[data-cy="gallery-item"]').should("have.length", 10);
      cy.get('[data-cy="gallery-item"]').first().should("be.visible");
    });

    it("should display initial gallery items with correct structure", () => {
      cy.get('[data-cy="gallery-item"]', { timeout: 10000 }).should("have.length", 10);

      cy.get('[data-cy="gallery-item"]').each(($item) => {
        cy.wrap($item).within(() => {
          // 1. Image
          cy.get('[data-cy="gallery-item-image"]').should("be.visible").and("have.attr", "src").and("not.be.empty");

          // 2. The app logo
          cy.get('[data-cy="gallery-item-app-logo"]')
            .should("be.visible")
            .and("have.attr", "src")
            .and("include", "galaxy_logo.svg");

          // 3. Title
          cy.get('[data-cy="gallery-item-title"]').should("be.visible").and("not.be.empty");

          // 4. The like or unlike action
          const heartAndCountContainer = cy.get('[data-cy="gallery-item-action"]');
          heartAndCountContainer.should("be.visible");
          heartAndCountContainer.find("i.fa-heart").should("be.visible");

          // Check if the like/unlike count is a number
          const likeUnlikeContainer = cy.get('[data-cy="gallery-item-unlike-or-like"]');
          likeUnlikeContainer.invoke("text").should("match", /\d+/);

          // 5. The image credit
          cy.get('[data-cy="gallery-item-image-credit"]')
            .should("be.visible")
            .and("contain.text", "Image credit:")
            .find("b")
            .next()
            .should("not.be.empty");

          // 6. Posted date
          cy.get('[data-cy="gallery-item-date"]')
            .should("be.visible")
            .parent()
            .should("contain.text", "Posted:")
            .and("contain.text", "on");

          // 7. Link to APOD
          cy.get('[data-cy="gallery-item-apod-link"]')
            .should("be.visible")
            .and("have.text", "APOD")
            .and("have.attr", "href", "https://apod.nasa.gov/")
            .and("have.attr", "target", "_blank");
        });
      });
    });

    it("should show the modal with image details and correct structure when an item is clicked", () => {
      cy.get('[data-cy="gallery-item"]', { timeout: 10000 }).should("have.length.at.least", 1);
      cy.get('[data-cy="gallery-item"]').first().find('[data-cy="gallery-item-image"]').click();
      cy.wait(1000);

      cy.get('[data-cy="image-details-modal"]')
        .should("be.visible")
        .within(() => {
          // Modal header elements
          // 1. App logo
          cy.get('[data-cy="modal-app-logo"]')
            .should("be.visible")
            .and("have.attr", "src")
            .and("include", "galaxy_logo.svg");

          // 2. Heart and count container
          const modalHeartContainer = cy.get('[data-cy="modal-heart-and-count-container"]');
          modalHeartContainer.should("be.visible");
          modalHeartContainer.find("i.fa-heart").should("be.visible");

          const likeCountContainer = cy.get('[data-cy="modal-like-count-text-container"]');
          likeCountContainer.invoke("text").should("match", /\d+/);

          // 3. Download icon
          cy.get('[data-cy="modal-download-icon"]').should("be.visible");
          // 4. Close icon
          cy.get('[data-cy="modal-close-icon"]').should("be.visible");

          // Modal body elements
          cy.get(".modal-body").within(() => {
            // 5. Title
            cy.get('[data-cy="modal-title"]').should("be.visible").and("not.be.empty");
            // 6. Image
            cy.get('[data-cy="modal-image"]').should("be.visible").and("have.attr", "src").and("not.be.empty");

            // 7. Explanation
            cy.get('[data-cy="modal-explanation"]')
              .scrollIntoView()
              .should("be.visible")
              .and("contain.text", "Explanation:")
              .invoke("text")
              .then((text) => {
                expect(text.trim()).not.to.be.empty;
              });

            // 8. Image credit
            cy.get('[data-cy="modal-image-credit"]')
              .scrollIntoView()
              .should("be.visible")
              .and("contain.text", "Image credit:")
              .invoke("text")
              .then((fullText) => {
                const authorName = fullText.replace("Image credit:", "").trim();
                expect(authorName).not.to.be.empty;
              });

            // 9. Posted date
            cy.get('[data-cy="modal-posted-date"]')
              .scrollIntoView()
              .should("be.visible")
              .parent()
              .should("contain.text", "Posted:")
              .and("contain.text", "on");

            // 10. APOD link
            cy.get('[data-cy="modal-apod-link"]')
              .scrollIntoView()
              .should("be.visible")
              .and("have.text", "APOD")
              .and("have.attr", "href", "https://apod.nasa.gov/");
          });
        });

      cy.get('[data-cy="modal-close-icon"]').click();
      cy.get('[data-cy="image-details-modal"]').should("not.be.visible");
    });
  });

  describe("Search functionality", () => {
    it("should display search results when a query is entered", () => {
      cy.intercept("GET", "/api/v1/search/*/0/10/").as("searchRequest");
      cy.get('[data-cy="search-input"]').type("Mars{enter}");
      cy.wait("@searchRequest");
      cy.get('[data-cy="gallery-item"]').should("have.length.greaterThan", 0);
    });

    it("should show no results for keywords that do not match anything", () => {
      cy.intercept("GET", "/api/v1/search/*/0/10/").as("searchRequest");
      cy.get('[data-cy="search-input"]').type("xx{enter}");
      cy.wait("@searchRequest");
      cy.get('[data-cy="gallery-item"]').should("have.length", 0);
      cy.get('[data-cy="no-results-message"]').should("be.visible").and("contain.text", "No images found");
    });
  });
});
