<template>
      <div class="loginform">
        <input type="text" v-model="login" placeholder="Логин">
        <input type="password" v-model="password" placeholder="Пароль">
        <button @click="registrate" class="submitButton regist">Регистрация</button>
        <button @click="authorize" class="submitButton">Подтвердить</button>
      </div>
</template>

<script>
  import $ from 'jquery'
    export default {
      name: "Login",
      data () {
        return {
          login: '',
          password: ''
        }
      },
      methods: {
        authorize () {
          $.ajax({
            url: 'http://127.0.0.1:8000/auth/login/',
            type: 'POST',
            data: {
              username: this.login,
              password: this.password
            },
            success: (responce) => {
              sessionStorage.access = responce.access
              sessionStorage.refresh = responce.refresh
              sessionStorage.username = responce.user.username
              this.$router.push({name: 'home'})
            },
            error: (responce) => {
              if (responce.status === 400) {
                alert('Неверный логин или пароль!')
              }
            }
          })
        },
        registrate: function () {
          this.$emit('authchange', false)
        }
      }

    }
</script>

<style >
  @import "./../assets/style/auth.css";
</style>
