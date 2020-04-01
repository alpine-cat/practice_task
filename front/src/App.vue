<template>
  <div id="app">
    <div id="background"></div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
  @import "assets/style/reset.css";
  @import "./assets/style/auth.css";
  #background {
    background-image: url("./assets/background.png") ;
    background-size: cover;
    min-height: 100%;
    min-width: 100%;
    position: absolute;
    z-index: -1;
  }

  #app {
    max-height: 100%;
    overflow: hidden;
  }

</style>
