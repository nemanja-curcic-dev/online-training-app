<template>
  <div id="exercise">
    <div v-if="exercise">
      {{exercise.name}}
      {{exercise.description}}
    </div>
  </div>
</template>

<script>
    export default {
      name: "Exercise",
      data (){
        return {
          exercise: null
        }
      },
      props: ['exercise_name'],
      created(){
        fetch('/clients/exercise_by_name/?name=' + this.exercise_name, {
          method: 'GET',
          headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
          }
        }).then(resp => {
          resp.json().then(data => {
            this.exercise = data;
          })
        })
      }
    }
</script>

<style scoped>

</style>
