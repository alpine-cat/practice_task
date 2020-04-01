<template>
<div>

  <div class="container">
    <div v-if="auth"><Login v-on:authchange = "changeAuthState"></Login></div>
    <div v-else><Regist v-on:authchange = "changeAuthState"></Regist></div>
  </div>
</div>
</template>

<script>
    import Login from "./Login";
    import Regist from "./Regist";
    export default {
      name: "auth",
      components: {Regist, Login},
      data() {
        return {
          auth: true,
        }
      },
      created() {
        sessionStorage.clear()
      },
      methods: {
        changeAuthState(state) {
          this.auth = state
        }
      }
    }
</script>

<style>
  @import "./../assets/style/auth.css";

  #app {
    max-height: 100vh;
    overflow: hidden;
  }

</style>
