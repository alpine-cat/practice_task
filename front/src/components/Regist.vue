<template>
  <div class="loginform">
    <input type="text" v-model="login" placeholder="Логин" >
    <input type="email" v-model="email" placeholder="E-mail">
    <input type="password" v-model="password1" placeholder="Пароль">
    <input type="password" v-model="password2" placeholder="Подтвердите пароль">
    <button @click="authorize" class="submitButton regist">Авторизация</button>
    <button @click="registrate" class="submitButton ">Подтвердить</button>
  </div>
</template>

<script>
  import $ from 'jquery'
    export default {
      name: "Regist",
      data () {
        return {
          login: '',
          email: '',
          password1: '',
          password2: ''
        }
      },
      methods: {
        authorize: function () {
          this.$emit('authchange', true)
        },
        registrate () {
          $.ajax({
            url: 'http://127.0.0.1:8000/auth/registration/',
            type: 'POST',
            data: {
              username: this.login,
              password1: this.password1,
              email: this.email,
              password2: this.password2

            },
            success: (response) => {
              sessionStorage.username = response.user.username
              sessionStorage.token = response.token
              sessionStorage.user_id = response.user.pk
              this.$router.push({name: 'home'})
            },
            error: (response) => {
              console.log(response)
              if (response.status === 400) {
                alert('Проверьте правильность введенных данных!')
              }
            }
          })
        }
      }
    }
</script>

<style>
  @import "./../assets/style/auth.css";

</style>
