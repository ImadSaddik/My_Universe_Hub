import { faker } from "@faker-js/faker";

export const createMockArchiveItem = () => {
  const image_likes_count = faker.number.int({ min: 0, max: 10 });
  const image_is_liked = image_likes_count > 0 && faker.datatype.boolean({ probability: 0.5 });
  const liked_by_users =
    image_is_liked && image_likes_count > 0
      ? Array.from({ length: image_likes_count }, () => faker.internet.email())
      : [];

  return {
    date: faker.date.recent({ days: 30 }).toISOString().split("T")[0],
    title: faker.lorem.sentence({ min: 3, max: 7 }),
    explanation: faker.lorem.paragraphs(faker.number.int({ min: 1, max: 3 })),
    image_url: faker.image.urlLoremFlickr({ category: "space,galaxy,nebula", width: 1024, height: 768 }),
    image_is_liked,
    image_likes_count,
    liked_by_users,
    comments: [],
    authors: `${faker.person.fullName()}${faker.datatype.boolean() ? `, ${faker.company.name()}` : ""}`,
  };
};

export const createMockArchiveList = (count = 10) => Array.from({ length: count }, createMockArchiveItem);

export const createMockArchiveCount = (customCount) => ({
  count: customCount ?? faker.number.int({ min: 50, max: 5000 }),
});
