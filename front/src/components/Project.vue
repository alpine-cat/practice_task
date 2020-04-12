<template>
  <div class="proj-contain" v-if="seen">
    <div class="projcolor" v-bind:style="{ backgroundColor: color}"></div>
  <input v-on:change="changeState" :id="$props.project.text+$props.project.id" type="radio"  :value="$props.project.text" name="project">
  <label :for="$props.project.text+$props.project.id">{{$props.project.text}}</label>
    <button v-on:click="edit" class="editdel"><img src="./../assets/edit.png"></button>
    <button v-on:click="delet" class="editdel"><img src="./../assets/delete.png"></button>
  </div>
  <div v-else>
    <input v-model="proj_color" class="proj_color" type="color">
    <input type="text" v-model='proj'>
    <button @click="editProject" class="addButton">Редактировать</button>
    <button @click="cancel" class="addButton">Отмена</button>
  </div>
</template>

<script>
  import $ from 'jquery'
    export default {
      name: "Project",
      props: ['project'],
      data(){
        return {
          color: this.$props.project.color,
          seen: true,
          proj_color: '',
          new_proj: this.$props.project.text,
          proj: ''
        }
      },
      methods:{
        changeState () {

          this.$emit('change', {id:this.$props.project.id, name: this.$props.project.text})
        },
        edit(){
          this.seen=false
        },
        cancel(){
          this.seen=true
        },
        delet(){
          $.ajax({
            url: `http://127.0.0.1:8000/tasks/?project=${this.$props.project.id}&date_ch=&status=False&owner=${sessionStorage.username}`,
            type: 'GET',
            success: (response) => {
              console.log(response)
              if(response.length > 0)
              {
                alert("Невозможно удалить проект, так как есть незавершенные задачи!")
              }else{
                $.ajax(
                  {
                    url: this.$props.project.url,
                    type: 'DELETE',
                    success: (response)=>{
                      alert("Проект удален!")
                      this.$router.go(0)
                    }
                  })
              }
            }
          })

        },
        editProject(){
          $.ajax(
            {
              url: this.$props.project.url,
              type: 'PUT',
              data: {
                'project_name': this.proj,
                'color': this.proj_color,
                'tasks': []
              },
              success: (response) => {
                this.$router.go(0)
              },
              error: (response) => {
                this.refreshTokens()
              }

            }
          )
        }
      }
    }
</script>
<style >
@import './../assets/style/main.css';
</style>
