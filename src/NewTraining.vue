<template>
  <div id="new_training">
      <table id="new_trainings_table">
        <thead>
        <tr>
          <th></th>
          <th>Exercise</th>
          <th>Resistance</th>
          <th>Sets</th>
          <th>Reps</th>
        </tr>
        </thead>
        <tbody v-for="(training, index) in trainings" :key="index" v-show="index === show">
          <tr v-for="(exercise, ex_index) in training.exercises" :key="ex_index">
            <td>{{ex_index + 1}}.</td>
            <td>
              <a @click.prevent="showExercise(ex_index + 1)" href="#">{{exercise.exercise}}</a>
              <exercise v-if="show_exercise === ex_index + 1" :exercise_name="exercise.exercise"></exercise>
            </td>
            <td>{{exercise.resistance}}</td>
            <td>{{exercise.sets}}</td>
            <td>{{exercise.reps}}</td>
          </tr>
          <tr>
             <td>
              <a target="_blank" :href="'/clients/do_training/?training_id=' + trainings[index].id + '&user_id=' + user_id"><button>Do training</button></a>
            </td>
          </tr>
        </tbody>
      </table>
      <div>
        <button :disabled="disablePrev" @click="changeTrainingSession(-1)">Prev</button>
        <button :disabled="disableNext" @click="changeTrainingSession(1)">Next</button>
      </div>
  </div>
</template>

<script>
    import Exercise from './Exercise'

    export default {
      name: "NewTraining",
      components: {
        exercise: Exercise
      },
      data () {
        return {
          trainings: [],
          show: 0,
          show_exercise: 0
        }
      },
      created () {
        fetch('/clients/training_sessions/?new=new', {
          method: 'GET',
          headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
          }
        }).then(resp => {
          resp.json().then(data => {
            for(let i = 0; i < data.length; i++) {
              this.trainings.push({
                exercises: data[i].exercises,
                id: data[i].id
              })
            }
          })
        })
      },
      props:['user_id'],
      methods: {
        changeTrainingSession(inc) {
          this.show += inc;
          this.show_exercise = 0;
        },
        showExercise(param) {
          if (this.show_exercise === param) {
            this.show_exercise = 0;
          } else {
            this.show_exercise = param;
          }
        }
      },
      computed: {
        disablePrev(){
          return this.show === 0;
        },
        disableNext(){
          return this.show === this.trainings.length - 1;
        }
      }
    }
</script>

<style>
 #new_trainings_table{
   margin: 0 auto;
 }
</style>
