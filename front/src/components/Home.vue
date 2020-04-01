<template>
  <div>
    <header>
      <div id="head">
        <div class="label-block"><h1>ToDo...</h1></div>
        <div class="username-block">
          <button @click="getArchive" class="addButton archive"><img src='./../assets/checklist.png'></button>
          <span>{{username}}</span>
          <button @click="onLogout" id="logout">Выйти</button>
        </div>
      </div>
    </header>
    <div class="container">
        <div class="menu-container">
          <div class="proj-contain menu ">
            <input @change="getToday" id="today" type="radio" value="Today" name="project" checked="checked">
            <label for="today">Сегодня</label></div>
          <div class=" proj-contain menu">
            <input @change="get7Days" id="seven_days" type="radio" value="Week" name="project">
            <label for="seven_days">Неделя</label></div>

          <div id="proj-container" v-for="project in projects">
            <Project @change = 'getTasks' v-bind:project = 'project' v-bind:key="project.id" ></Project>
          </div>
          <div v-if='add' style="margin-top: 20px;"><input v-model="proj_color" class="proj_color" type="color">
            <input type="text" v-model="new_proj" placeholder="Название проекта">
            <button @click="addProject" class="addButton">Добавить</button>
            <button @click="add = false" class="addButton">Отмена</button>
          </div>

          <div v-else ><button class="addButton" @click="add = true">Создать проект</button> </div>
        </div>
      <div class="task-container" >
        <div class="title"><h1>{{title}}</h1></div>
      <div v-for="task in tasks">
        <Task v-bind:task="task" v-bind:projects="projects" v-bind:key="task.id"></Task>
      </div>
        <div class="create" v-if="add_task" id="new_task">
          <input type="text" v-model="new_task" placeholder="Введите задание">
          <input type="date" v-model="task_date">
          <div style="margin: 5px">
            <label>Приоритет: </label>
          <select v-model="priority_select" value="Приоритет">
            <option v-for="p in priority" :value="p">{{p.text}}</option>
          </select>
          </div>
          <div style="margin:5px">
            <label>Проект: </label>
          <select v-model="project_name" value="Выберите проект">
            <option v-for="project in projects" :value="project">{{project.text}}</option>
          </select>
          </div>
          <button class="addButton" @click="addTask">Добавить</button>
          <button @click="add_task = false" class="addButton">Отмена</button>
        </div>
        <div class="create" v-else><button class="addButton" @click="add_task = true">Создать</button> </div>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jquery'
  import Project from "./Project";
  import Task from "./Task";
  import moment from 'moment'
    export default {
      name: "home",
      components: {Project, Task},
      data() {
        return {
          task_date: '',
          add_task: false,
          add:false,
          username: '',
          new_proj: '',
          projects: [],
          proj_color: '',
          tasks: [],
          new_task: '',
          priority: [
            {id:0, color:'red', text: 'Высокий'},
            {id:1, color:'orange', text: 'Средний'},
            {id:2, color:'white', text: 'Низкий'}
          ],
          title: '',
          project_name: '',
          priority_select: ''
        }
      },
      created() {
        if (!sessionStorage.username) {
          this.$router.push({name: 'auth'})
        }
        $.ajaxSetup({
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('access')}`
          }
        })
        this.username = sessionStorage.username
        this.getProjects()
        this.getToday()
      },
      methods: {
        refreshTokens(fun, args) {
          $.ajax({
            url: 'http://127.0.0.1:8000/auth/refresh/',
            type: 'POST',
            data: {
              'refresh': sessionStorage.refresh
            },
            success: (responce) => {
              sessionStorage.access = responce.access
              if(args)
                fun(args)
              else
                fun()
            },
            error: (responce) => {
              this.onLogout()
            }
          })
        },
        onLogout() {
          sessionStorage.clear()
          $.ajaxSetup({
            headers: {
              'Authorization': ''
            }
          })
          this.$router.push({name: 'auth'})
        },
        getTasks(args){
          this.title = args.name;
          this.tasks = [];

          $.ajax({
            url: `http://127.0.0.1:8000/tasks/?project=${args.id}&date_ch=&status=False&owner=${sessionStorage.username}`,
            type: 'GET',
            success: (responce) => {
              console.log(responce)
              for (let t in responce) {
                this.setColorByPriority(responce[t])
              }
            },
            error: (responce) => {
              this.refreshTokens(this.getTasks, {value, name})
            }
          })
        },
        getProjects() {
          $.ajax({
            url: 'http://127.0.0.1:8000/projects',
            type: 'GET',
            success: (responce) => {
              for (let v in responce) {
                this.projects.push(
                  {id: responce[v].id,
                    text: responce[v].project_name,
                    color: responce[v].color,
                    url: responce[v].url})

              }
            },
            error: (responce) => {
              this.refreshTokens(this.getProjects)
            }
          })
        },
        getToday() {
          this.title = 'Сегодня'
          this.tasks = []

          let date = moment().format("YYYY-MM-DD");

          console.log(date)
          $.ajax({
            url: `http://127.0.0.1:8000/tasks/?project=&date_ch=${date}&status=False&owner=${sessionStorage.username}`,
            type: 'GET',
            success: (responce) => {
                console.log(responce)
                for (let t in responce) {
                  this.setColorByPriority(responce[t])
                }

            },
            error: (responce) => {
              this.refreshTokens(this.getToday)
            }
          })
        },
        get7Days() {
          this.title = 'Неделя'
          this.tasks = []
          let date = moment().add(7, 'days').format("YYYY-MM-DD");

          $.ajax({
            url: `http://127.0.0.1:8000/tasks/?project=&date_ch=${date}&status=False&owner=${sessionStorage.username}`,
            type: 'GET',
            success: (responce) => {

                for (let t in responce) {
                  this.setColorByPriority(responce[t])

              }
            },
            error: (responce) => {
              this.refreshTokens(this.get7Days)
            }
          })
        },
        addProject() {
          if (this.new_proj !== '') {
            $.ajax({
              url: 'http://127.0.0.1:8000/projects/',
              type: 'POST',
              data: {
                'project_name': this.new_proj,
                'color': this.proj_color,
                'tasks': []
              },
              success: (responce) => {
                this.add = false
                this.$router.go(0)
              },
              error: (responce) => {
                this.refreshTokens(this.addProject)
              }
            })
          }

        },
        addTask(){

          console.log(this.priority_select)
          console.log('hey')
          $.ajax({
            url: 'http://127.0.0.1:8000/tasks/',
            type: 'POST',
            data: {
              project: this.project_name.url,
              task: this.new_task,
              date: moment(this.task_date).format("YYYY-MM-DD"),
              priority: this.priority_select.id,
              status: 'False'
            },
            success: (responce) => {
              this.$router.go(0)
            },
            error: (responce) => {
              this.refreshTokens(this.saveTask)
              alert('Перепроверьте правильность введенных данных или перезагрузите страницу.')
            }
          })
        },
        getArchive(){
          this.title = 'Архив'
          this.tasks = []
          $.ajax({
            url: `http://127.0.0.1:8000/tasks/?project=&date_ch=&status=True&owner=${sessionStorage.username}`,
            type: 'GET',
            success: (responce) => {

              for (let t in responce) {

                this.setColorByPriority(responce[t])

              }
            },
            error: (responce) => {
              this.refreshTokens(this.getArchive)
            }
          })
        },
        setColorByPriority(task){
          let textcolor = ''
          let color = ''
          if(task.priority===0) color = 'red'
          else if (task.priority===1) color = 'orange'
          else color = 'white'
          if(moment().format("YYYY-MM-DD")>task.date) {
            textcolor = 'red'
            this.tasks.unshift({
              id: task.id,
              url: task.url,
              task: task.task,
              project: task.project,
              priority: task.priority,
              color: color,
              textcolor: textcolor,
              date: task.date,
              status: task.status
            })
          }
          else {
            textcolor = 'black'

            this.tasks.push({
              id: task.id,
              url: task.url,
              task: task.task,
              project: task.project,
              priority: task.priority,
              color: color,
              textcolor: textcolor,
              date: task.date,
              status: task.status
            })
          }
        }
      }
    }
</script>

<style>
  @import "./../assets/style/main.css";
  #app {
    height: 100%;
    overflow: visible;
  }
  #background{
    background-image: none;
    background-color: #d1c8dd;
    opacity: 0.6;
    height: 100%;
  }
</style>
