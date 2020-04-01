<template>
    <div v-if="add" class="task">
      <div id="priority" v-bind:style="{ backgroundColor: color}"></div>
        <div class="taskContent"><span v-bind:style="{color: textcolor}">{{$props.task.task}}</span>
        <span class="taskDate">{{$props.task.date}}</span></div>


      <div class="editTask"><button v-on:click="add = false" class=""><img src="./../assets/edit.png"></button>
      <button v-on:click="deleteTask" class=""><img src="./../assets/delete.png"></button></div>
      <div class="statusContainer"><label for="taskstatus">status</label>
      <input id="taskstatus" type="checkbox" @change="editStatus" :checked="$props.task.status"></div>
    </div>
  <div v-else>
    <input type="text" v-model="new_task">
    <input type="date" v-model="task_date">
    <select v-model="priority_select">
      <option v-for="p in priority" :value="p">{{p.text}}</option>
    </select>
    <select v-model="project_name">
      <option v-for="project in $props.projects" :value="project">{{project.text}}</option>
    </select>
    <button class="addButton" @click="saveTask">Сохранить</button>
    <button @click="add = true" class="addButton">Отмена</button>
  </div>
</template>

<script>
  import $ from 'jquery'
  import moment from 'moment'
    export default {
        name: "Task",
      props:['task', 'projects'],
      data(){
          return{
            color:this.$props.task.color,
            textcolor: this.$props.task.textcolor,
            add: true,
            priority: [
              {id:0, color:'red', text: 'Высокий'},
              {id:1, color:'orange', text: 'Средний'},
              {id:2, color:'white', text: 'Низкий'}
            ],
            new_task: this.$props.task.task,
            task_date: this.$props.task.date,
            project_name: this.$props.task.project,
            priority_select: this.$props.task.priority
          }
      },
      methods: {
          saveTask(){
            $.ajax({
              url: this.$props.task.url,
              type: 'PUT',
              data: {
                project: this.project_name.url,
                task: this.new_task,
                date: moment(this.task_date).format("YYYY-MM-DD"),
                priority: this.priority_select.id,
                status: 'False'
              },
              success: (responce) =>
              {
                this.$router.go(0)
              },
              error: (responce) =>
              {
                alert('Перепроверьте правильность введенных данных или перезагрузите страницу.')

              }
            })

          },
          deleteTask(){
            $.ajax(
              {
                url: this.$props.task.url,
                type: 'DELETE',
                success: (responce)=>{
                  alert("Задача удалена!")
                  this.$router.go(0)
                }
              })
          },
          editStatus(){
            console.log(this.$props.task.priority)
            console.log('heeeeeeeeeey')
            $.ajax({
              url: this.$props.task.url,
              type: 'PUT',
              data: {
                project: this.$props.task.project,
                task: this.$props.task.task,
                date: this.$props.task.date,
                status: !this.$props.task.status?'True':'False',
                priority: this.$props.task.priority
              },
              success: (responce) => {
                this.$router.go(0)
              },
              error: (responce) => {
                console.log(responce)
                alert('Упс.. что-то пошло не так. Перезагрузите страницу и попробуйте еще')
              }
            })
          }
      }
    }
</script>

<style>
  #priority{
    height: 40px;
    width: 10px;
    float: left;
    margin-right: 10px;
  }
</style>
