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
          <div style="margin:5px 0"><label for="task_status">Статус</label>
          <input id="task_status" type="checkbox" v-model="task_status" @change="taskStatusChanged">
          </div>
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
          priority_select: '',
          task_status: 'True'
        }
      },
      created() {
        if (!sessionStorage.username) {
          this.$router.push({name: 'auth'})
        }
        $.ajaxSetup({
          headers: {
           'Authorization': `${sessionStorage.getItem('token')}`
          }
        })
        this.username = sessionStorage.username
        this.getProjects()
        this.getToday()
      },
      methods: {

        onLogout() {
          sessionStorage.clear()
          $.ajaxSetup({
            headers: {
              'Authorization': ''
            }
          })
          this.$router.push({name: 'auth'})
        },
        taskStatusChanged(){
        console.log(this.task_status)
        if(this.task_status==='False')
          this.task_status = 'True'
         else
          this.task_status = 'False'
        },
        getTasks(args){
          this.title = args.name;
          this.tasks = [];
          console.log(args.id)
          $.ajax({
            url: `http://127.0.0.1:8000/tasks/?project=${args.id}&date_ch=&status=False&owner=${sessionStorage.username}`,
            type: 'GET',
            success: (response) => {
              console.log(response)
              for (let t in response) {
                this.setColorByPriority(response[t])
              }
            },
            error: (response) => {
            }
          })
        },
        getProjects() {
          $.ajax({
            url: `http://127.0.0.1:8000/projects/?owner=${sessionStorage.username}`,
            type: 'GET',
            success: (response) => {
              for (let v in response) {
                this.projects.push(
                  {id: response[v].id,
                    text: response[v].project_name,
                    color: response[v].color,
                    url: response[v].url})

              }
            },
            error: (response) => {
            console.log(response)
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
            success: (response) => {
                console.log(response)
                for (let t in response) {
                  this.setColorByPriority(response[t])
                }

            },
            error: (response) => {
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
            success: (response) => {

                for (let t in response) {
                  this.setColorByPriority(response[t])

              }
            },
            error: (response) => {
            }
          })
        },
        addProject() {
          if (this.new_proj !== '') {
            $.ajax({
              url: 'http://127.0.0.1:8000/projects/',
              type: 'POST',
              data: {
                'owner': 'http://127.0.0.1:8000/users/'+sessionStorage.user_id+'/',
                'project_name': this.new_proj,
                'color': this.proj_color,
                'tasks': []
              },
              success: (response) => {
                this.add = false
                this.$router.go(0)
              },
              error: (response) => {
              console.log(response)
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
              status: this.task_status
            },
            success: (response) => {
              this.$router.go(0)
            },
            error: (response) => {
              alert('Проверьте правильность введенных данных.')
            }
          })
        },
        getArchive(){
          this.title = 'Архив'
          this.tasks = []
          $.ajax({
            url: `http://127.0.0.1:8000/tasks/?project=&date_ch=&status=True&owner=${sessionStorage.username}`,
            type: 'GET',
            success: (response) => {

              for (let t in response) {

                this.setColorByPriority(response[t])

              }
            },
            error: (response) => {
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
