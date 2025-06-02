describe("Acknowledgement Bar", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("should display the APOD link correctly", () => {
    const apodLink = cy.get('[data-test="apod-link"]');

    apodLink.should("be.visible");
    apodLink.should("have.text", "APOD");
    apodLink.should("have.attr", "href", "https://apod.nasa.gov/");
    apodLink.should("have.attr", "target", "_blank");
    apodLink.should("have.attr", "rel", "noopener noreferrer");
  });

  it("should contain the full acknowledgement text from fixture", () => {
    cy.fixture("acknowledgementText.json").then((textFixture) => {
      cy.get("[data-cy='acknowledgement-text']").should("contain.text", textFixture.text);
    });
  });
});
