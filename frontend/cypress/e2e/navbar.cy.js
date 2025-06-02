describe("Home Page", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("should display the correct title", () => {
    cy.title().should("eq", "Home");
  });

  describe("Navigation bar", () => {
    it("shows the logo in the navigation bar", () => {
      cy.get('[data-test="nav-link-app-logo"]').should("be.visible");
    });

    it("should show the 'home' text in bold in the navigation bar", () => {
      cy.get('[data-test="nav-link-home"]').should("have.css", "font-weight", "700");
      cy.get('[data-test="nav-link-today"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-trending"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-favourites"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-contribute"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-about"]').should("have.css", "font-weight", "400");
    });

    it("should show all navigation links", () => {
      cy.get('[data-test="nav-link-home"]').should("be.visible");
      cy.get('[data-test="nav-link-today"]').should("be.visible");
      cy.get('[data-test="nav-link-trending"]').should("be.visible");
      cy.get('[data-test="nav-link-favourites"]').should("be.visible");
      cy.get('[data-test="nav-link-contribute"]').should("be.visible");
      cy.get('[data-test="nav-link-about"]').should("be.visible");
    });

    it("shows the GitHub link", () => {
      cy.get('[data-cy="github-link"]').should("be.visible");
      cy.get('[data-test="github-star-count"]').should("be.visible");
    });

    it("shows the log in button", () => {
      cy.get('[data-test="nav-link-login"]').should("be.visible");
      cy.get('[data-test="nav-link-login"]').contains("Log In");
      cy.get('[data-test="nav-link-logout"]').should("not.be.visible");
    });

    it("shows the correct tooltip on hovering the login button", () => {
      const loginButton = cy.get('[data-test="nav-link-login"]');
      const expectedTooltipText = "Log In";

      loginButton.trigger("mouseover");
      cy.get("div.tooltip-inner").should("be.visible").and("have.text", expectedTooltipText);

      loginButton.trigger("mouseout");
      cy.get("div.tooltip-inner").should("not.exist");
    });

    it("shows the correct tooltip on hovering the GitHub link", () => {
      const githubLink = cy.get('[data-cy="github-link"]');
      const expectedTooltipText = "GitHub repository";

      githubLink.trigger("mouseover");
      cy.get("div.tooltip-inner").should("be.visible").and("have.text", expectedTooltipText);

      githubLink.trigger("mouseout");
      cy.get("div.tooltip-inner").should("not.exist");
    });

    it("checks all hrefs in the navigation bar", () => {
      cy.get('[data-test="nav-link-home"]').should("have.attr", "href", "/");
      cy.get('[data-test="nav-link-today"]').should("have.attr", "href", "/today");
      cy.get('[data-test="nav-link-trending"]').should("have.attr", "href", "/trending");
      cy.get('[data-test="nav-link-favourites"]').should("have.attr", "href", "/favourites");
      cy.get('[data-test="nav-link-about"]').should("have.attr", "href", "/about");
      cy.get('[data-test="nav-link-contribute"]').should("have.attr", "href", "/contribute");
      cy.get('[data-cy="github-link"]').should("have.attr", "href").and("include", "github.com");
      cy.get('[data-test="nav-link-login"]').should("have.attr", "href", "/login");
    });
  });

  describe("Clicking navigation links", () => {
    it("should navigate to the 'Today' page", () => {
      cy.get('[data-test="nav-link-today"]').click();
      cy.url().should("include", "/today");
      cy.title().should("eq", "Today's Picture");

      cy.get('[data-test="nav-link-today"]').should("have.css", "font-weight", "700");
      cy.get('[data-test="nav-link-home"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-trending"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-favourites"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-about"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-contribute"]').should("have.css", "font-weight", "400");
    });

    it("should navigate to the 'Trending' page", () => {
      cy.get('[data-test="nav-link-trending"]').click();
      cy.url().should("include", "/trending");
      cy.title().should("eq", "Trending");

      cy.get('[data-test="nav-link-trending"]').should("have.css", "font-weight", "700");
      cy.get('[data-test="nav-link-home"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-today"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-favourites"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-about"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-contribute"]').should("have.css", "font-weight", "400");
    });

    it("should navigate to the 'Favourites' page", () => {
      cy.get('[data-test="nav-link-favourites"]').click();
      cy.url().should("include", "/favourites");
      cy.title().should("eq", "Favourites");

      cy.get('[data-test="nav-link-favourites"]').should("have.css", "font-weight", "700");
      cy.get('[data-test="nav-link-home"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-today"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-trending"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-about"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-contribute"]').should("have.css", "font-weight", "400");
    });

    it("should navigate to the 'Contribute' page", () => {
      cy.get('[data-test="nav-link-contribute"]').click();
      cy.url().should("include", "/contribute");
      cy.title().should("eq", "Contribute");

      cy.get('[data-test="nav-link-contribute"]').should("have.css", "font-weight", "700");
      cy.get('[data-test="nav-link-home"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-today"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-trending"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-favourites"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-about"]').should("have.css", "font-weight", "400");
    });

    it("should navigate to the 'About' page", () => {
      cy.get('[data-test="nav-link-about"]').click();
      cy.url().should("include", "/about");
      cy.title().should("eq", "About");

      cy.get('[data-test="nav-link-about"]').should("have.css", "font-weight", "700");
      cy.get('[data-test="nav-link-home"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-today"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-trending"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-favourites"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-contribute"]').should("have.css", "font-weight", "400");
    });

    it("should navigate to the 'Home' page after clicking the logo", () => {
      cy.get('[data-test="nav-link-app-logo"]').click();
      cy.url().should("include", "/");
      cy.title().should("eq", "Home");

      cy.get('[data-test="nav-link-home"]').should("have.css", "font-weight", "700");
      cy.get('[data-test="nav-link-today"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-trending"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-favourites"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-about"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-contribute"]').should("have.css", "font-weight", "400");
    });

    it("should navigate to the 'Login' page", () => {
      cy.get('[data-test="nav-link-login"]').click();
      cy.url().should("include", "/login");
      cy.title().should("eq", "Log In");

      cy.get('[data-test="nav-link-home"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-today"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-trending"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-favourites"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-about"]').should("have.css", "font-weight", "400");
      cy.get('[data-test="nav-link-contribute"]').should("have.css", "font-weight", "400");
    });
  });
});
