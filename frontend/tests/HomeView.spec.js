import axios from "axios";
import { createStore } from "vuex";
import { flushPromises, mount } from "@vue/test-utils";
import HomeView from "@/views/HomeView.vue";
import { beforeEach, describe, it, expect, vi } from "vitest";
import { afterEach } from "vitest";
import { createMockArchiveList, createMockArchiveCount, createMockArchiveItem } from "./factories/mockDataFactory";

let mockSetSelectedNavbarItem;

const createMockStore = (initialState = {}) => {
  const defaultState = {
    token: "",
    selectedNavbarItem: "home",
    apodStatus: "up",
  };

  mockSetSelectedNavbarItem = vi.fn((state, item) => {
    state.selectedNavbarItem = item;
  });

  return createStore({
    state() {
      const state = { ...defaultState, ...initialState };
      return state;
    },
    mutations: {
      setSelectedNavbarItem: mockSetSelectedNavbarItem,
    },
  });
};

const getWrapper = (store) => {
  return mount(HomeView, {
    global: {
      plugins: [store],
      stubs: {
        SearchSection: true,
        GallerySection: true,
        BackToTopVue: true,
        ImageDetails: true,
      },
    },
  });
};

vi.mock("axios", () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: [] })),
    defaults: { headers: { common: {} } },
  },
}));

const getLocalStorageMock = () => {
  return {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
  };
};

describe("HomeView", () => {
  let store;
  /** @type {import('@vue/test-utils').VueWrapper<any>} */
  let wrapper;
  let localStorageMock;

  beforeEach(() => {
    document.title = "";
    store = createMockStore();

    localStorageMock = getLocalStorageMock();
    global.localStorage = localStorageMock;
    vi.spyOn(localStorageMock, "setItem");
    vi.spyOn(localStorageMock, "removeItem");
    vi.spyOn(localStorageMock, "getItem");
    vi.spyOn(localStorageMock, "clear");
  });

  afterEach(() => {
    vi.clearAllMocks();
    if (wrapper) {
      wrapper.unmount();
      wrapper = null;
    }
  });

  describe("created hook", () => {
    it("sets the document title to 'Home' on created", () => {
      wrapper = getWrapper(store);
      expect(document.title).toBe("Home");
    });

    it("commits 'setSelectedNavbarItem' to 'home' on created", () => {
      wrapper = getWrapper(store);
      expect(mockSetSelectedNavbarItem).toHaveBeenCalledTimes(1);
      expect(mockSetSelectedNavbarItem).toHaveBeenCalledWith(expect.anything(), "home");
    });
  });

  describe("mounted hook", () => {
    it("calls getArchive and getArchiveSize on mounted and updates data", async () => {
      const mockArchiveData = createMockArchiveList(10);
      const mockArchiveSizeData = createMockArchiveCount();

      axios.get.mockResolvedValueOnce({ data: mockArchiveData }).mockResolvedValueOnce({ data: mockArchiveSizeData });
      wrapper = getWrapper(store);
      await flushPromises();

      expect(axios.get).toHaveBeenCalledTimes(2);
      expect(axios.get).toHaveBeenCalledWith("/api/v1/gallery/0/10/");
      expect(axios.get).toHaveBeenCalledWith("/api/v1/gallery/count/");

      expect(wrapper.vm.archive).toEqual(mockArchiveData);
      expect(wrapper.vm.archiveSize).toBe(mockArchiveSizeData.count);
    });
  });

  describe("load more button", () => {
    it("should show load more button when there are more items to load", async () => {
      const mockArchiveData = createMockArchiveList(10);
      const mockArchiveSizeData = createMockArchiveCount();

      axios.get.mockResolvedValueOnce({ data: mockArchiveData }).mockResolvedValueOnce({ data: mockArchiveSizeData });
      wrapper = getWrapper(store);
      await flushPromises();

      expect(wrapper.vm.shouldShowLoadMoreButton).toBe(true);
    });

    it("should not show load more button when archive data length is greater than or equal to archive count", async () => {
      const mockArchiveData = createMockArchiveList(10);
      const mockArchiveSizeData = createMockArchiveCount(5);

      axios.get.mockResolvedValueOnce({ data: mockArchiveData }).mockResolvedValueOnce({ data: mockArchiveSizeData });
      wrapper = getWrapper(store);
      await flushPromises();

      expect(wrapper.vm.shouldShowLoadMoreButton).toBe(false);
    });
  });

  describe("authentication", () => {
    it("checks if user is logged off", () => {
      wrapper = getWrapper(store);
      expect(wrapper.vm.isUserLoggedOff).toBe(true);
    });

    it("checks if user is not logged off when token is present", () => {
      const store = createMockStore({ token: "fake-token" });
      wrapper = getWrapper(store);
      expect(wrapper.vm.isUserLoggedOff).toBe(false);
    });
  });

  describe("search", () => {
    it("fetches search results when a non-empty query is provided", async () => {
      const searchQuery = "galaxy";
      const mockSearchResults = createMockArchiveList(10);
      const mockSearchCount = createMockArchiveCount(50);

      axios.get
        .mockResolvedValueOnce({ data: createMockArchiveList(0) })
        .mockResolvedValueOnce({ data: createMockArchiveCount(0) });

      wrapper = getWrapper(store);
      await flushPromises();

      axios.get.mockClear();

      axios.get.mockResolvedValueOnce({ data: mockSearchCount }).mockResolvedValueOnce({ data: mockSearchResults });

      await wrapper.vm.search(searchQuery);
      await flushPromises();

      expect(wrapper.vm.query).toBe(searchQuery);
      expect(wrapper.vm.archive).toEqual([]);
      expect(wrapper.vm.searchArchive).toEqual(mockSearchResults);
      expect(wrapper.vm.searchArchiveSize).toBe(mockSearchCount.count);

      expect(axios.get).toHaveBeenCalledTimes(2);
      expect(axios.get).toHaveBeenCalledWith(`/api/v1/search/${searchQuery}/count/`);
      expect(axios.get).toHaveBeenCalledWith(`/api/v1/search/${searchQuery}/0/10/`);
    });

    it("fetches gallery archive when search query is empty", async () => {
      // 1. Simulate that we have already fetched the gallery archive
      const initialArchive = createMockArchiveList(10);
      const initialArchiveCount = createMockArchiveCount(20);
      axios.get.mockResolvedValueOnce({ data: initialArchive }).mockResolvedValueOnce({ data: initialArchiveCount });

      wrapper = getWrapper(store);
      await flushPromises();

      expect(axios.get).toHaveBeenCalledTimes(2);
      expect(axios.get).toHaveBeenCalledWith("/api/v1/gallery/0/10/");
      expect(axios.get).toHaveBeenCalledWith("/api/v1/gallery/count/");

      expect(wrapper.vm.archive).toEqual(initialArchive);
      expect(wrapper.vm.archiveSize).toBe(initialArchiveCount.count);

      // 2. Simulate a search query with a non-empty string
      const searchQuery = "star";
      const mockSearchResults = createMockArchiveList(10);
      const mockSearchCount = createMockArchiveCount(50);

      axios.get.mockClear();
      axios.get.mockResolvedValueOnce({ data: mockSearchCount }).mockResolvedValueOnce({ data: mockSearchResults });
      await wrapper.vm.search(searchQuery);
      await flushPromises();

      expect(wrapper.vm.query).toBe(searchQuery);
      expect(wrapper.vm.archive).toEqual([]);
      expect(wrapper.vm.searchArchive).toEqual(mockSearchResults);
      expect(wrapper.vm.searchArchiveSize).toBe(mockSearchCount.count);

      expect(axios.get).toHaveBeenCalledTimes(2);
      expect(axios.get).toHaveBeenCalledWith(`/api/v1/search/${searchQuery}/count/`);
      expect(axios.get).toHaveBeenCalledWith(`/api/v1/search/${searchQuery}/0/10/`);

      // 3. Call the search method with an empty string and ensure that we fall back to the gallery archive
      const finalGalleryData = createMockArchiveList(10);

      axios.get.mockClear();
      axios.get.mockResolvedValueOnce({ data: finalGalleryData });
      await wrapper.vm.search("");
      await flushPromises();

      expect(wrapper.vm.query).toBe("");
      expect(wrapper.vm.searchArchive).toEqual([]);
      expect(wrapper.vm.archive).toEqual(finalGalleryData);

      expect(axios.get).toHaveBeenCalledTimes(1);
      expect(axios.get).toHaveBeenCalledWith("/api/v1/gallery/0/10/");
    });
  });

  describe("increase limit", () => {
    it("fetches more gallery items when query is empty", async () => {
      // 1. Initial setup: mounted hook fetches initial data
      const initialArchiveItems = createMockArchiveList(10);
      const totalArchiveSize = createMockArchiveCount(20);
      axios.get.mockResolvedValueOnce({ data: initialArchiveItems }).mockResolvedValueOnce({ data: totalArchiveSize });

      wrapper = getWrapper(store);
      await flushPromises();

      expect(wrapper.vm.archive.length).toBe(10);
      axios.get.mockClear();

      // 2. Setup for increaseLimit: mock response for the next batch of items
      const additionalArchiveItems = createMockArchiveList(10);
      axios.get.mockResolvedValueOnce({ data: additionalArchiveItems });

      // 3. Call increaseLimit
      await wrapper.vm.increaseLimit();
      await flushPromises();

      expect(axios.get).toHaveBeenCalledTimes(1);
      expect(axios.get).toHaveBeenCalledWith("/api/v1/gallery/10/20/");
      expect(wrapper.vm.archive.length).toBe(20); // 10 initial + 10 additional

      const expectedFullArchive = [...initialArchiveItems, ...additionalArchiveItems];
      expect(wrapper.vm.archive).toEqual(expectedFullArchive);
    });

    it("fetches more search results when query is active", async () => {
      // 1. Set archive and archiveSize to initial values
      const initialArchiveItems = createMockArchiveList(10);
      const totalArchiveSize = createMockArchiveCount(20);
      axios.get.mockResolvedValueOnce({ data: initialArchiveItems }).mockResolvedValueOnce({ data: totalArchiveSize });

      wrapper = getWrapper(store);
      await flushPromises();

      expect(wrapper.vm.archive.length).toBe(10);
      expect(wrapper.vm.archiveSize).toBe(totalArchiveSize.count);

      // 2. Simulate a search query
      const searchQuery = "stars";
      const initialSearchItems = createMockArchiveList(10);
      const totalSearchSize = createMockArchiveCount(20);

      axios.get.mockClear();
      axios.get.mockResolvedValueOnce({ data: totalSearchSize }).mockResolvedValueOnce({ data: initialSearchItems });
      await wrapper.vm.search(searchQuery);
      await flushPromises();

      expect(wrapper.vm.searchArchive.length).toBe(10);
      expect(wrapper.vm.searchArchiveSize).toBe(totalSearchSize.count);

      // 3. Call increaseLimit
      const additionalSearchItems = createMockArchiveList(10);

      axios.get.mockClear();
      axios.get.mockResolvedValueOnce({ data: totalSearchSize }).mockResolvedValueOnce({ data: additionalSearchItems });
      await wrapper.vm.increaseLimit();
      await flushPromises();

      expect(axios.get).toHaveBeenCalledTimes(2);
      expect(axios.get).toHaveBeenCalledWith(`/api/v1/search/${searchQuery}/count/`);
      expect(axios.get).toHaveBeenCalledWith(`/api/v1/search/${searchQuery}/10/20/`);
      expect(wrapper.vm.searchArchive.length).toBe(20); // 10 initial + 10 additional

      const expectedFullSearchArchive = [...initialSearchItems, ...additionalSearchItems];
      expect(wrapper.vm.searchArchive).toEqual(expectedFullSearchArchive);
    });
  });

  describe("remove likes", () => {
    it("removes likes from an archive", async () => {
      const mockArchiveList = createMockArchiveList(10);
      wrapper = getWrapper(store);
      const updatedArchive = wrapper.vm.removeLikes(mockArchiveList);
      expect(updatedArchive.every((item) => item.image_is_liked === false)).toBe(true);
    });

    it("removes likes from an empty archive", async () => {
      const mockArchiveList = [];
      wrapper = getWrapper(store);
      const updatedArchive = wrapper.vm.removeLikes(mockArchiveList);
      expect(updatedArchive.every((item) => item.image_is_liked === false)).toBe(true);
    });
  });

  describe("update archive likes", () => {
    const userEmail = "imad.saddik@test.com";

    it("should return an empty array if the input archive is empty", () => {
      wrapper = getWrapper(store);
      const updatedArchive = wrapper.vm.updateArchiveLikes([]);
      expect(updatedArchive).toEqual([]);
    });

    it("should not change image_is_liked if user email is not in localStorage", () => {
      localStorageMock.getItem.mockReturnValue(null);
      wrapper = getWrapper(store);
      wrapper.vm.incrementSize = 10;

      const initialArchive = createMockArchiveList(10);
      const updatedArchive = wrapper.vm.updateArchiveLikes([...initialArchive]);

      // Expect image_is_liked to remain unchanged because no user email to check against
      expect(updatedArchive.every((item) => item.image_is_liked === false)).toBe(true);
      expect(localStorageMock.getItem).toHaveBeenCalledWith("email");
    });

    it("should correctly update image_is_liked based on user email in localStorage", () => {
      localStorageMock.getItem.mockReturnValue(userEmail);
      wrapper = getWrapper(store);
      wrapper.vm.incrementSize = 10;

      let archive = createMockArchiveList(4);
      archive[0].liked_by_users.push(userEmail);
      archive[2].liked_by_users.push(userEmail);
      archive[3].liked_by_users = null;
      archive.push(null);

      const result = wrapper.vm.updateArchiveLikes([...archive]);

      expect(result[0].image_is_liked).toBe(true);
      expect(result[1].image_is_liked).toBe(false);
      expect(result[2].image_is_liked).toBe(true);
      expect(result[3].image_is_liked).toBe(false);
      expect(result[4]).toBe(null);
      expect(localStorageMock.getItem).toHaveBeenCalledWith("email");
    });
  });
});
