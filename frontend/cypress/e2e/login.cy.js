describe("Login Feature", () => {
  it("should login successfully and redirect to home", () => {
    // 1. Visit home and check title
    cy.visit("/");
    cy.title().should("eq", "Home");

    // 2. Click login button and check title
    cy.get('[data-test="nav-link-login"]').click();
    cy.title().should("eq", "Log In");

    // 3. Fill in credentials from environment variables and submit
    cy.get('[data-cy="login-email"]').type(Cypress.env("TEST_USER_EMAIL"));
    cy.get('[data-cy="login-password"]').type(Cypress.env("TEST_USER_PASSWORD"));
    cy.get('[data-cy="login-submit"]').click();

    // 4. Should be redirected to home
    cy.url().should("eq", `${Cypress.config().baseUrl}/`);
    cy.title().should("eq", "Home");
  });
});
