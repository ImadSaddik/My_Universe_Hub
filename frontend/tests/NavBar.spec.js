import { describe, it, expect, beforeEach, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createStore } from "vuex";
import NavBar from "@/components/NavBar.vue";
import axios from "axios";

vi.mock("axios", () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: { stargazers_count: 3647 } })),
    defaults: { headers: { common: {} } },
  },
}));

const createMockStore = (initialState = {}) => {
  const defaultState = {
    token: "",
    email: "",
    selectedNavbarItem: "home",
  };

  return createStore({
    state() {
      const state = { ...defaultState, ...initialState };
      return state;
    },
    mutations: {
      removeToken: vi.fn((state) => {
        state.token = "";
      }),
      removeEmail: vi.fn((state) => {
        state.email = "";
      }),
      setSelectedNavbarItem: vi.fn((state, item) => {
        state.selectedNavbarItem = item;
      }),
    },
  });
};

const getWrapper = (store) => {
  return mount(NavBar, {
    global: {
      plugins: [store],
    },
  });
};

const getLocalStorageMock = () => {
  return {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
  };
};

describe("NavBar.vue", () => {
  let store;
  /** @type {import('@vue/test-utils').VueWrapper<any>} */
  let wrapper;
  let localStorageMock;

  beforeEach(() => {
    axios.defaults.headers.common.Authorization = undefined;

    store = createMockStore();
    vi.spyOn(store, "commit");

    localStorageMock = getLocalStorageMock();
    global.localStorage = localStorageMock;
    vi.spyOn(localStorageMock, "setItem");
    vi.spyOn(localStorageMock, "removeItem");
    vi.spyOn(localStorageMock, "getItem");
    vi.spyOn(localStorageMock, "clear");

    wrapper = getWrapper(store);
  });

  it("returns the correct email from getEmail computed property", () => {
    const testEmail = "user@example.com";
    store = createMockStore({ email: testEmail });
    wrapper = getWrapper(store);
    expect(wrapper.vm.getEmail).toBe(testEmail);
  });

  it("renders all main navigation links", () => {
    const expectedLinkSelectors = [
      "nav-link-home",
      "nav-link-today",
      "nav-link-trending",
      "nav-link-favourites",
      "nav-link-contribute",
      "nav-link-about",
    ];
    expectedLinkSelectors.forEach((selector) => {
      expect(wrapper.find(`[data-testid="${selector}"]`).exists()).toBe(true);
    });
  });

  it("renders the retrieved number of stars", async () => {
    const starCount = wrapper.find("[data-testid='github-star-count']");
    expect(starCount.exists()).toBe(true);
    expect(starCount.text()).toBe("3647");
  });

  it("renders log in button and hides log out button when not authenticated", () => {
    const loginLink = wrapper.find("[data-testid='nav-link-login']");
    expect(loginLink.exists()).toBe(true);
    expect(loginLink.isVisible()).toBe(true);
    expect(loginLink.text()).toBe("Log In");

    const logoutLink = wrapper.find("[data-testid='nav-link-logout']");
    expect(logoutLink.exists()).toBe(true);
    expect(logoutLink.isVisible()).toBe(false);
    expect(logoutLink.text()).toBe("Log Out");
  });

  it("renders log out button and hides log in button when authenticated", () => {
    store = createMockStore({ token: "fake-token" });
    wrapper = getWrapper(store);

    const loginLink = wrapper.find("[data-testid='nav-link-login']");
    expect(loginLink.exists()).toBe(true);
    expect(loginLink.isVisible()).toBe(false);

    const logoutLink = wrapper.find("[data-testid='nav-link-logout']");
    expect(logoutLink.exists()).toBe(true);
    expect(logoutLink.isVisible()).toBe(true);
    expect(logoutLink.text()).toBe("Log Out");
  });

  it("emits logged-out event and clears localStorage and store when log out button is clicked", async () => {
    const logoutLink = wrapper.find("[data-testid='nav-link-logout']");
    await logoutLink.trigger("click");
    expect(wrapper.emitted("logged-out")).toBeTruthy();
    expect(localStorageMock.removeItem).toHaveBeenCalledWith("token");
    expect(localStorageMock.removeItem).toHaveBeenCalledWith("email");
  });

  it("renders the app logo", () => {
    const logo = wrapper.find("[data-testid='app-logo']");
    expect(logo.exists()).toBe(true);
    expect(logo.attributes("src")).toBe("/src/assets/logos/galaxy_logo.svg");
  });

  it("calls handleNavbarItemClick and updates localStorage when 'About' link is clicked", async () => {
    const aboutLink = wrapper.find("[data-testid='nav-link-about']");
    expect(aboutLink.exists()).toBe(true);

    const handleNavbarItemClickSpy = vi.spyOn(wrapper.vm, "handleNavbarItemClick");
    await aboutLink.trigger("click");

    // Check CSS class for active link
    expect(aboutLink.classes()).toContain("active");

    // Check that the localStorage was updated
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(1);
    expect(localStorageMock.setItem).toHaveBeenCalledWith("selectedNavbarItem", wrapper.vm.ABOUT_PAGE);

    // Check that the method was called with the correct argument
    expect(handleNavbarItemClickSpy).toHaveBeenCalledTimes(1);
    expect(handleNavbarItemClickSpy).toHaveBeenCalledWith(wrapper.vm.ABOUT_PAGE);
  });

  it("calls handleNavbarItemClick and updates localStorage when 'Contribute' link is clicked", async () => {
    const contributeLink = wrapper.find("[data-testid='nav-link-contribute']");
    expect(contributeLink.exists()).toBe(true);

    const handleNavbarItemClickSpy = vi.spyOn(wrapper.vm, "handleNavbarItemClick");
    await contributeLink.trigger("click");

    // Check CSS class for active link
    expect(contributeLink.classes()).toContain("active");

    // Check that the localStorage was updated
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(1);
    expect(localStorageMock.setItem).toHaveBeenCalledWith("selectedNavbarItem", wrapper.vm.CONTRIBUTE_PAGE);

    // Check that the method was called with the correct argument
    expect(handleNavbarItemClickSpy).toHaveBeenCalledTimes(1);
    expect(handleNavbarItemClickSpy).toHaveBeenCalledWith(wrapper.vm.CONTRIBUTE_PAGE);
  });

  it("calls handleNavbarItemClick and updates localStorage when 'Favourites' link is clicked", async () => {
    const favouritesLink = wrapper.find("[data-testid='nav-link-favourites']");
    expect(favouritesLink.exists()).toBe(true);

    const handleNavbarItemClickSpy = vi.spyOn(wrapper.vm, "handleNavbarItemClick");
    await favouritesLink.trigger("click");

    // Check CSS class for active link
    expect(favouritesLink.classes()).toContain("active");

    // Check that the localStorage was updated
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(1);
    expect(localStorageMock.setItem).toHaveBeenCalledWith("selectedNavbarItem", wrapper.vm.FAVOURITES_PAGE);

    // Check that the method was called with the correct argument
    expect(handleNavbarItemClickSpy).toHaveBeenCalledTimes(1);
    expect(handleNavbarItemClickSpy).toHaveBeenCalledWith(wrapper.vm.FAVOURITES_PAGE);
  });

  it("calls handleNavbarItemClick and updates localStorage when 'Trending' link is clicked", async () => {
    const trendingLink = wrapper.find("[data-testid='nav-link-trending']");
    expect(trendingLink.exists()).toBe(true);

    const handleNavbarItemClickSpy = vi.spyOn(wrapper.vm, "handleNavbarItemClick");
    await trendingLink.trigger("click");

    // Check CSS class for active link
    expect(trendingLink.classes()).toContain("active");

    // Check that the localStorage was updated
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(1);
    expect(localStorageMock.setItem).toHaveBeenCalledWith("selectedNavbarItem", wrapper.vm.TRENDING_PAGE);

    // Check that the method was called with the correct argument
    expect(handleNavbarItemClickSpy).toHaveBeenCalledTimes(1);
    expect(handleNavbarItemClickSpy).toHaveBeenCalledWith(wrapper.vm.TRENDING_PAGE);
  });

  it("calls handleNavbarItemClick and updates localStorage when 'Today' link is clicked", async () => {
    const todayLink = wrapper.find("[data-testid='nav-link-today']");
    expect(todayLink.exists()).toBe(true);

    const handleNavbarItemClickSpy = vi.spyOn(wrapper.vm, "handleNavbarItemClick");
    await todayLink.trigger("click");

    // Check CSS class for active link
    expect(todayLink.classes()).toContain("active");

    // Check that the localStorage was updated
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(1);
    expect(localStorageMock.setItem).toHaveBeenCalledWith("selectedNavbarItem", wrapper.vm.TODAY_PAGE);

    // Check that the method was called with the correct argument
    expect(handleNavbarItemClickSpy).toHaveBeenCalledTimes(1);
    expect(handleNavbarItemClickSpy).toHaveBeenCalledWith(wrapper.vm.TODAY_PAGE);
  });

  it("calls handleNavbarItemClick and updates localStorage when 'Home' link is clicked", async () => {
    const homeLink = wrapper.find("[data-testid='nav-link-home']");
    expect(homeLink.exists()).toBe(true);

    const handleNavbarItemClickSpy = vi.spyOn(wrapper.vm, "handleNavbarItemClick");
    await homeLink.trigger("click");

    // Check CSS class for active link
    expect(homeLink.classes()).toContain("active");

    // Check that the localStorage was updated
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(1);
    expect(localStorageMock.setItem).toHaveBeenCalledWith("selectedNavbarItem", wrapper.vm.HOME_PAGE);

    // Check that the method was called with the correct argument
    expect(handleNavbarItemClickSpy).toHaveBeenCalledTimes(1);
    expect(handleNavbarItemClickSpy).toHaveBeenCalledWith(wrapper.vm.HOME_PAGE);
  });

  it("calls handleNavbarItemClick and updates localStorage when 'App logo' link is clicked", async () => {
    const appLogoLink = wrapper.find("[data-testid='nav-link-app-logo']");
    expect(appLogoLink.exists()).toBe(true);

    const handleNavbarItemClickSpy = vi.spyOn(wrapper.vm, "handleNavbarItemClick");
    await appLogoLink.trigger("click");

    // Check that the localStorage was updated
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(1);
    expect(localStorageMock.setItem).toHaveBeenCalledWith("selectedNavbarItem", wrapper.vm.HOME_PAGE);

    // Check that the method was called with the correct argument
    expect(handleNavbarItemClickSpy).toHaveBeenCalledTimes(1);
    expect(handleNavbarItemClickSpy).toHaveBeenCalledWith(wrapper.vm.HOME_PAGE);
  });

  it("checks if the 'About' link has the correct to", () => {
    const aboutLink = wrapper.find("[data-testid='nav-link-about']");
    expect(aboutLink.attributes("to")).toBe("/about");
  });

  it("checks if the 'Contribute' link has the correct to", () => {
    const contributeLink = wrapper.find("[data-testid='nav-link-contribute']");
    expect(contributeLink.attributes("to")).toBe("/contribute");
  });

  it("checks if the 'Favourites' link has the correct to", () => {
    const favouritesLink = wrapper.find("[data-testid='nav-link-favourites']");
    expect(favouritesLink.attributes("to")).toBe("/favourites");
  });

  it("checks if the 'Trending' link has the correct to", () => {
    const trendingLink = wrapper.find("[data-testid='nav-link-trending']");
    expect(trendingLink.attributes("to")).toBe("/trending");
  });

  it("checks if the 'Today' link has the correct to", () => {
    const todayLink = wrapper.find("[data-testid='nav-link-today']");
    expect(todayLink.attributes("to")).toBe("/today");
  });

  it("checks if the 'Home' link has the correct to", () => {
    const homeLink = wrapper.find("[data-testid='nav-link-home']");
    expect(homeLink.attributes("to")).toBe("/");
  });

  it("checks if the 'App logo' link has the correct to", () => {
    const appLogoLink = wrapper.find("[data-testid='nav-link-app-logo']");
    expect(appLogoLink.attributes("to")).toBe("/");
  });

  it("clears axios Authorization header on logout", async () => {
    // Set an initial token to simulate a logged-in state for the store
    // and an initial Authorization header for axios
    const initialToken = "fake-test-token";
    store = createMockStore({ token: initialToken, email: "test@example.com" });
    wrapper = getWrapper(store);

    // Set an initial Authorization header on the mocked axios
    axios.defaults.headers.common.Authorization = `Token ${initialToken}`;

    // Ensure the logout button is visible and click it
    const logoutButton = wrapper.find("[data-testid='nav-link-logout']");
    expect(logoutButton.exists()).toBe(true);
    expect(logoutButton.isVisible()).toBe(true);

    await logoutButton.trigger("click");
    // Check that the Authorization header on the mocked axios is cleared
    expect(axios.defaults.headers.common.Authorization).toBe("");
  });
});
