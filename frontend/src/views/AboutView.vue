<template>
  <section class="container pt-2 pt-sm-5 mb-5">
    <div class="row">
      <h1 class="custom-title-text">My Universe Hub</h1>
    </div>
    <div class="row mt-4">
      <p class="custom-small-text">
        Hello astro enthusiasts! I'm Imad Saddik, and I'm obsessed with astronomy. I stumbled into this amazing field when I was 19, and honestly, discovering the wonders of the universe has been the best thing that's ever happened to me.
      </p>
      <p class="custom-small-text">
        I absolutely love looking at the stunning images shared by NASA, ESA, CSA, and even amateur or professional astronomers on the internet. One of my favorite places to go is <a href="https://apod.nasa.gov/apod/archivepix.html">APOD</a> (Astronomy Picture Of the Day). What's cool about APOD is that you never know what you're gonna get each day. It's like a little surprise waiting for you every time you visit.
      </p>
      <p class="custom-small-text">
        The image below is a star trail I captured when I visited my grand parents in the countryside in 2024. The sky was so clear that I could see the faint Milky Way arm that passes through <a href="https://en.wikipedia.org/wiki/Cygnus_(constellation)">Cygnus</a> with my naked eye. I set up my phone and took hundreds of small exposure shots, and this is what I got. I hope you like it!
      </p>
    </div>
    <div class="row mt-4 d-flex justify-content-center">
      <div class="col col-lg-6">
        <img class="img-fluid rounded-4" src="../assets/about_page/StarTrails_20240818055242_720p.jpeg" alt="">
        <p class="text-center m-0 mt-2">Star trails over Oued Amlil, Morocco, August 18, 2024</p>
      </div>
    </div>
    <div class="row mt-5">
      <p class="custom-small-text">
        After months of using APOD, I started thinking, "Hey, this site looks a bit outdated." Since I've been learning web development, I had this crazy idea: Why not give APOD a modern look? That's how "My Universe Hub" was born!
      </p>
      <p class="custom-small-text">
        This little project of mine is my baby. I've invested hundreds of hours and over a year of work into it. When I showed it to a few friends, they were like, "Imad, you have to share this with the world!" But I was kinda nervous about it. I mean, I didn't know anything about deploying websites, and I was just a student back then with no income.
      </p>
      <p class="custom-small-text">
        Fast forward to after graduation and landing a job, I finally took the plunge. I learned how to deploy a website, and yey! "My Universe Hub" is now live for everyone to enjoy. By the way, if you're feeling generous and want to help keep this site running, check out the <RouterLink to="/contribute">contribute</RouterLink> page.
      </p>
      <p class="custom-small-text">
        The image below is a shot of Orion I took in another Countryside close to Bir Tam Tam in Morocco in 2024. That night was a little bit cloudy. Nevertheless, I set up my phone and took a long exposure shot or Orion behind the cloud, and this is what I got.
      </p>
    </div>
    <div class="row mt-4 d-flex justify-content-center">
      <div class="col col-lg-6">
        <img class="img-fluid rounded-4" src="../assets/about_page/Orion_20240129_210527_720p.jpeg" alt="">
        <p class="text-center m-0 mt-2">Orion over Bir Tam Tam, Morocco, January 29, 2024</p>
      </div>
    </div>
    <div class="row mt-5 d-flex flex-column justify-content-center">
      <p class="custom-small-text">
        I have to admit, I was a bit scared about using all these images that aren't mine. But, I've made sure to give proper credit to the original creators, whether it's NASA, ESA, or any other agency or astronomer. Just to be clear, I'm not in this for the money or anything. I just really love astronomy and APOD, and I saw a chance to make it even better for fellow space enthusiasts.
      </p>
      <p class="custom-small-text">
        Oh, and guess what? "My Universe Hub" is open-source! You can find the code on <a href="https://github.com/ImadSaddik/My_Universe_Hub">GitHub</a> and more info on the <RouterLink to="/contribute">contribute</RouterLink> page. I'd be over the moon if people wanted to share ideas, help develop new features, translate the site, or spread the word. Let's build an awesome community together!
      </p>
      <p class="custom-small-text">
        So come on in, explore the universe with us, and let's geek out over the cosmos together!
        Speaking of community, we've got a Discord server you can join. Just click <a href="https://discord.gg/nADvHzQyvZ">here</a> to hang out with your fellow astro enthusiasts. Remember, be cool and friendly! 
      </p>
    </div>
    <div class="row mt-4 d-flex justify-content-center">
      <div class="col col-lg-6">
        <img class="img-fluid rounded-4" src="../assets/about_page/LunarEclipse_20240918_134431_1024p.png" alt="">
        <p class="text-center m-0 mt-2">Orion over Bir Tam Tam, Morocco, January 29, 2024</p>
      </div>
    </div>
    <div class="row mt-5 d-flex flex-column justify-content-center">
      <p class="custom-small-text">
        Here's one final image before I leave. This is a shot of a lunar eclipse I took in 2024. I was in Meknes, my birthplace. I remeber sleeping only 3 hours that day because I was eager to witness my first lunar eclipse. Enjoy!
      </p>
    </div>
  </section>
</template>

<script>
import { RouterLink } from 'vue-router';

export default {
  name: "AboutView",
};
</script>
