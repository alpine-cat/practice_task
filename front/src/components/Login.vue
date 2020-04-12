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
            success: (response) => {
            console.log(response)
              sessionStorage.token = response.token
              sessionStorage.username = response.user.username
              sessionStorage.user_id = response.user.pk
              this.$router.push({name: 'home'})
            },
            error: (response) => {
              console.log(response)
              alert('Неверный логин или пароль!')
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
