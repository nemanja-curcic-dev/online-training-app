<template>
  <div id="new_training">
      <button @click="getTrainingData">Trening</button>
  </div>
</template>

<script>
    export default {
      name: "NewTraining",
      data () {
        return {

        }
      },
      methods: {
        getTrainingData () {
          fetch('/clients/training_sessions', {
            method: 'GET',
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }
          }).then(resp => {
            resp.json().then(data => {
              console.log(data);
            })
          })
        }
      }
    }
</script>

<style scoped>

</style>
