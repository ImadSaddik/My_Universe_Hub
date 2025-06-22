import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import AcknowledgementBar from "@/components/AcknowledgementBar.vue";

describe("AcknowledgementBar", () => {
  const wrapper = mount(AcknowledgementBar);

  it("contains the link to APOD", () => {
    const link = wrapper.find("[data-testid='apod-link']");
    expect(link.exists()).toBe(true);
    expect(link.attributes("href")).toBe("https://apod.nasa.gov/");
    expect(link.text()).toBe("APOD");
  });
});
