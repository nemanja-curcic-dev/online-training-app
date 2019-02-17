<template>
  <div id="do_training" class="col-md-8 col-md-offset-2 col-sm-12 col-xs-12">
    <div id="training-table-wrapper">
      <table id="do_trainings_table">
        <thead>
        <tr>
          <th></th>
          <th>Exercise</th>
          <th>Resistance</th>
          <th>Sets</th>
          <th>Reps</th>
          <th>Eval</th>
        </tr>
        </thead>
        <tbody v-for="(row, index) in training" :key="index">
            <tr >
              <td>{{index + 1}}.</td>
              <td>
                <a @click.prevent="showExerciseDesc(index + 1)" href="#">{{row.exercise.exercise}}</a>
              </td>
              <td>{{row.exercise.resistance}}</td>
              <td>{{row.exercise.sets}}</td>
              <td>{{row.exercise.reps}}</td>
              <td :id="'evaluate_button' + index" @click="showDifficulty(index + 1)"><i style="cursor: pointer;" class="glyphicon glyphicon-ok"></i></td>
            </tr>
            <tr>
              <td colspan="6" v-if="show_exercise === index + 1">
                <div>
                  <div class="instructions">
                    <h4>Instructions</h4>
                    <p v-html="row.desc.instructions">{{row.desc.instructions}}</p>
                  </div>
                  <div class="instructions">
                   <img :src="row.desc.img_link" alt="">
                 </div>
                </div>
              </td>
            </tr>
            <tr>
              <td colspan="6" v-if="show_evaluate_exercise === index + 1">
                <div @click="evaluateExercise(index, 'easy')" class="evaluate easy">Easy</div>
                <div @click="evaluateExercise(index, 'right')" class="evaluate right">Just right</div>
                <div @click="evaluateExercise(index, 'hard')" class="evaluate hard">Hard</div>
                <div @click="evaluateExercise(index, 'too_hard')" class="evaluate too_hard">Too hard</div>
              </td>
            </tr>
        </tbody>
        <tr>
          <td colspan="6">
           <div>
            <p style="color: red;" v-show="check_all">Please evaluate all exercises before submitting training.</p>
          </div>
          <div style="display: flex;">
            <div style="flex-grow: 1;"><button class="btn btn-primary" @click="submitTraining">Submit training</button></div>
            <div style="flex-grow: 1;">
              <button v-if="!show_timer" @click="trainingTimer" class="btn btn-primary">Start timer <i class="glyphicon glyphicon-time"></i></button>
              <div v-if="show_timer">
                <p style="font-weight: bold;">{{formatTime(computedTimePassed)}} <i class="glyphicon glyphicon-time"></i></p>
                <label for="submit-time">Submit time</label>
                <input id="submit-time" type="checkbox" v-model="submit_time">
              </div>
            </div>
          </div>
          </td>
        </tr>
      </table>
    </div>
    <modals-container>
    </modals-container>
    <div class="col-md-8 col-md-offset-2 col-sm-12 col-xs-12 charts">
       <select class="form-control" title="exercise-select" id="select-exercise" @change="getExerciseData" v-model="exercise_name">
         <option :value="null" disabled selected>Check resistances for previous sessions</option>
         <option v-for="(row, index) in training" :key="index" :value="row.exercise.exercise">{{row.exercise.exercise}}</option>
        </select>
      <div style="margin-top: 12px; border-top: 1px solid #eeee;">
         <bar-chart v-for="(data, key) in computedChartData" :key="key" :chart-data="data" :height="250" v-if="show_chart"></bar-chart>
      </div>
    </div>
  </div>
</template>

<script>
    import LineChart from './charts/LineChartComponent'
    import BarChart from './charts/BarChartComponent'
    import OkModal from './modals/OkModal'

    export default {
      name: "DoTraining",
      props: ['training_id', 'user_id', 'user_name'],
      components: {
        'line-chart': LineChart,
        'bar-chart': BarChart
      },
      data(){
        return {
          training: null,
          show_exercise: 0,
          show_evaluate_exercise: 0,
          evaluation: {},
          check_all: false,
          exercise_name: null,
          show_chart: false,
          chartData: null,
          time_passed: 0,
          show_timer: false,
          submit_time: false
        }
      },
      computed: {
        computedChartData(){
          return this.chartData;
        },
        computedTimePassed(){
          return this.time_passed;
        }
      },
      methods: {
        getExerciseData(){
          let self = this;

          fetch('/api/return_exercise_data', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              user_id: this.user_id,
              ex: this.exercise_name
            })
          }).then(resp => {
            resp.json().then(data => {
              self.show_chart = false;
              this.chartData = null;

              let tempChartData = {
                total: {
                  labels: [],
                  datasets: [
                    {
                      label: 'total (sets x reps x weight)',
                      backgroundColor: '#286090',
                      data: [],
                    }
                  ]
                },
                weight: {
                  labels: [],
                  datasets: [
                    {
                      label: 'weight (kg)',
                      backgroundColor: '#5cb85c',
                      data: []
                    }
                  ]
                },
                sets: {
                  labels: [],
                  datasets: [
                    {
                      label: 'sets',
                      backgroundColor: '#f4e842',
                      data: [],
                    }
                  ]
                },
                reps: {
                  labels: [],
                  datasets: [
                    {
                      label: 'reps',
                      backgroundColor: '#f87979',
                      data: [],
                    }
                  ]
                }
                };

              for(let key in data){
                if(data.hasOwnProperty(key)){
                  tempChartData.sets.labels.push(key);
                  tempChartData.sets.datasets[0].data.push(data[key][0]);

                  tempChartData.reps.labels.push(key);
                  tempChartData.reps.datasets[0].data.push(data[key][1]);

                  if(data[key][2] !== 0){
                    tempChartData.weight.labels.push(key);
                    tempChartData.weight.datasets[0].data.push(data[key][2]);
                  }

                  tempChartData.total.labels.push(key);

                  tempChartData.total.datasets[0].data.push(data[key][3]);
                }
              }

              if(tempChartData.weight.datasets[0].data.length === 0 && tempChartData.weight.labels.length === 0){
                delete tempChartData.weight;
              }

              self.chartData = tempChartData;
              self.show_chart = true;
            });
            })
          },
        submitTraining(){
          let evalLen = 0;
          let self = this;

          for(let key in this.evaluation){
            if (this.evaluation.hasOwnProperty(key)){
              evalLen++;
            }
          }

          let body = {};

          if (this.submit_time) {
            body = {
                evaluated: this.evaluation,
                training_id: this.training_id,
                training_time: this.time_passed
              }
          } else {
            body = {
                evaluated: this.evaluation,
                training_id: this.training_id
              };
          }

          if (evalLen < this.training.length){
            this.check_all = true;
          } else{
            fetch('/submit_training', {
              method: 'POST',
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(body)
          }).then(resp => {
            resp.json().then(data => {
              if (data.status) {
                self.$modal.show(OkModal, {
                    name: self.user_name,
                  },
                  {
                    height: 'auto',
                    width: 250
                  },
                  {
                    'closed': (event) => {
                      window.location.replace(location.protocol + '//' + location.host + '/clients/training/new_training');
                    }
                  });
              }
            })
          });
          }
        },
        showExerciseDesc(param){
          if (this.show_exercise === param) {
            this.show_exercise = 0;
          } else {
            this.show_exercise = param;
          }
        },
        showDifficulty(param){
           if (this.show_evaluate_exercise === param) {
            this.show_evaluate_exercise = 0;
          } else {
            this.show_evaluate_exercise = param;
          }
        },
        evaluateExercise(index, value){
          this.evaluation[this.training[index].exercise.id] = value;

          this.showDifficulty(index + 1);

          document.getElementById("evaluate_button" + index.toString()).className = value;

          this.check_all = false;
        },
        trainingTimer(){
          let self = this;
          this.show_timer = true;

          setInterval(function () {
            self.time_passed++;
          }, 1000)
        },
        formatTime(seconds){
          let hours = parseInt(seconds / 3600).toString();
          let mins = parseInt(seconds / 60).toString();
          let secs = (seconds % 60).toString();

          if (hours.length < 2) {
            hours = '0' + hours;
          }

          if (mins.length < 2) {
            mins = '0' + mins;
          }

          if (secs.length < 2) {
            secs = '0' + secs;
          }

          return hours + ':' + mins +':' + secs;
        }
      },
      created(){
        fetch('/clients/training_session_by_id/?training_id=' + this.training_id, {
          method: 'GET',
          headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
          }
        }).then(resp => {
          resp.json().then(data => {
            this.training = data;
          })
        })
      }
    }
</script>

<style>
  #do_trainings_table{
    background: #eeee;
    margin: 1% 0;
    width: 100%;
  }

  #do_trainings_table tr{
    border-bottom: 1px solid white;
  }

  #do_trainings_table th, #do_trainings_table td{
    padding: 7px;
    text-align: center;
  }

  .evaluate{
    color: white;
    cursor: pointer;
    display: inline-block;
    padding: 5px;
    text-align: center;
    width: 24%;
  }

  .easy{
    background: #3cf251;
  }

  .right{
    background: #58bc89;
  }

  .hard{
    background: #cace4c;
  }

  .too_hard{
    background: #b7051d;
  }

  .charts{
    background: white;
    text-align: center;
  }

  .instructions{
    display: inline-block;
    font-weight: bold;
    width: 48%;
  }

  .instructions img{
    height: 70%;
    width: 70%;
  }

  .timer{
    background: white;
    padding: 7px;
    text-align: center;
  }

  select{
    text-align: center;
  }

  @media screen and (max-width: 568px){
    #do_trainings_table{
      font-size: 0.9em;
    }

    .instructions{
      width: 100%;
    }

    .instructions img{
      height: 100%;
      width: 100%;
    }
  }

  @media screen and (max-width: 366px){
    #do_trainings_table{
      font-size: 0.8em;
    }
  }
</style>
