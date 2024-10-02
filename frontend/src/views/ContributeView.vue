<template>
  <section class="container pt-2 pt-sm-5 mb-5">
    <div class="row">
      <h1 class="custom-title-text">Help support My Universe Hub!</h1>
    </div>
    <div class="row mt-4">
      <p class="custom-small-text">
        Hello astro enthusiasts! Want to be part of making the cosmos more accessible to everyone? It does not matter if you know how to code or not, there are many ways you can help support My Universe Hub. Here are a few ideas:
      </p>
    </div>
    <div class="row mt-4 d-flex justify-content-center">
      <div class="col col-lg-6">
        <img class="img-fluid rounded-4" src="../assets/contribute_page/Antennae_Biggs_960.jpg" alt="">
        <p class="text-center m-0 mt-2">The heart shaped antennae galaxies</p>
      </div>
    </div>
    <div class="row mt-4">
      <p class="custom-small-text">
        I adore this image, it is one of my favorites. It is the Antennae galaxies, also known as NGC 4038 and NGC 4039. They are a pair of interacting galaxies and are currently in the process of colliding and merging with each other. I am sending you this image as a token of my appreciation for your support. I hope you like it as much as I do.
        <br/>
        Remember, I <i class="fa-solid fa-heart"></i> you all!
      </p>
    </div>
    <div class="row mt-4">
      <h2 class="custom-subtitle-text">Spread the word</h2>
      <p class="custom-small-text">
        Love what we're doing? Share My Universe Hub with your friends, and fellow space enthusiasts. The more people know about us, the more we can grow and improve! Dont't forget that we do have a <a href="https://discord.gg/nADvHzQyvZ">discord</a> server you can join.
      </p>
    </div>
    <div class="row mt-3">
      <h2 class="custom-subtitle-text">Code contributions</h2>
      <p class="custom-small-text">
        My Universe Hub is open-source! You can find the code on <a href="https://github.com/ImadSaddik/My_Universe_Hub">GitHub</a>. The code is broken into two repositories, one for development (public) and the other one is for production (private).

        We are separating the two because, we want to keep the users data safely secured in the private repository. The <a href="https://github.com/ImadSaddik/My_Universe_Hub">development repository</a> is where we develop new features, fix bugs, and test new ideas. Once we are confident that the new feature is working as expected, we merge it into the production repository.
      </p>

      <p class="custom-small-text">
        <strong>- For developers:</strong> If you want to help us develop new features, fix bugs, or test new ideas, feel free to fork the <a href="https://github.com/ImadSaddik/My_Universe_Hub">development repository</a>, make your changes, and submit a pull request. We will review your changes and merge them into the production repository if they meet our standards.
      </p>
      <p class="custom-small-text">
        <strong>- For the rest:</strong> If you have an idea for a new feature, a bug to report, or a suggestion to make, feel free to open an issue in the <a href="https://github.com/ImadSaddik/My_Universe_Hub">development repository</a>. We will review your issue and work on it as soon as possible.
      </p>
    </div>
    <div class="row mt-3">
      <h2 class="custom-subtitle-text">Help in hosting the website</h2>
      <p class="custom-small-text">
        My Universe Hub is hosted on a machine provisioned from digital ocean. If the website grows and we need to upgrade the machine, we will need more funds to keep the website running. If you want to help us in hosting the website, you have a lot of options to donate.
      </p>
      <p class="custom-small-text">
        You can donate via the following platforms:
        <br/>
        <i class="fa-brands fa-paypal me-2"></i> <a href="https://paypal.me/ProGamer20177?country.x=MA&locale.x=en_US">Paypal</a>
        <br/>
        <i class="fa-brands fa-patreon me-2"></i> <a href="https://www.patreon.com/3CodeCamp">Patreon</a>
      </p>
    </div>
    <div class="row mt-3">
      <h2 class="custom-subtitle-text">Translation</h2>
      <p class="custom-small-text">
        My Universe Hub is currently available in just one language: English. If you are fluent in another language and want to help us translate the website, feel free to fork the <a href="https://github.com/ImadSaddik/My_Universe_Hub">development repository</a>, make the necessary changes, and submit a pull request.
      </p>
      <p class="custom-small-text">
        To translate the APOD entries, you can use <a href="https://en.wikipedia.org/wiki/Large_language_model">LLM</a>s (Large Language Models) if you are familiar with them, they are incredible at translating text. If you are not familiar with them, you can use <a href="https://translate.google.com/?sl=en&tl=ar&op=translate">Google Translate</a>, but be sure to review the translation to make sure it is accurate.
      </p>
    </div>
  </section>
</template>

<script>
export default {
  name: "ContributeView",
};
</script>