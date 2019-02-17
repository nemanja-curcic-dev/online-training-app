<template>
    <div id="statistics">
      <div class="col-md-8 col-md-offset-2 col-sm-12">
        <div class="nav-wrapper">
          <div @click="category = 1" class="nav-button btn btn-primary">Training history</div>
          <div @click="category = 2" class="nav-button btn btn-success btn btn-success">Test history</div>
          <div @click="category = 3" class="nav-button btn btn-info ">Load distribution</div>
        </div>
        <div class="calendar-wrapper" style="width: 40%">
          <!--<table id="calendar">
            <thead>
                <tr id="month">
                    <th style="text-align: center" colspan="1" ><a id="month_back" href="#">&lt&lt</a></th>
                    <th style="text-align: center" colspan="5" id="selected_month"></th>
                    <th style="text-align: center" colspan="1" ><a id="month_forward" href="#">&gt&gt</a></th>
                </tr>
                <tr id="days">
                    <th style="text-align: center; width: 14.2%">Mon</th>
                    <th style="text-align: center; width: 14.2%">Tue</th>
                    <th style="text-align: center; width: 14.2%">Wed</th>
                    <th style="text-align: center; width: 14.2%">Thu</th>
                    <th style="text-align: center; width: 14.2%">Fri</th>
                    <th style="text-align: center; width: 14.2%">Sat</th>
                    <th style="text-align: center; width: 14.2%">Sun</th>
                </tr>
            </thead>
            <tbody id="calendar_body">

            </tbody>
          </table>-->
        </div>
        <div v-if="category === 1" class="chart-wrapper">
          <line-chart v-if="chartData.labels.length !== 0 && chartData.datasets[0].data.length !== 0" :chart-data="chartData"></line-chart>
        </div>
        <div v-if="category === 2" class="chart-wrapper">
          <div class="nav-wrapper">
            <div @click="anthropometry_category = 1" class="nav-button btn btn-primary">Anthropometry</div>
            <div @click="anthropometry_category = 2" class="nav-button btn btn-success btn btn-success">Strength</div>
            <div class="nav-button btn btn-info">Endurance</div>
            <div class="nav-button btn btn-warning">Mobility</div>
          </div>

          <div v-if="anthropometry_category === 1">
            <bar-chart v-for="(data, index) in test_history.anthropometry" :key="index" :chart-data="data.chartData"></bar-chart>
          </div>

          <div v-if="anthropometry_category === 2">
            strength
          </div>

        </div>
      </div>
    </div>
</template>

<script>
    import LineChart from './charts/LineChartComponent'
    import BarChart from './charts/BarChartComponent'


    export default {
      name: "Statistics",
      components: {
        'line-chart': LineChart,
        'bar-chart': BarChart
      },
      data () {
        return {
          category: 1,
          anthropometry_category: 1,
          test_history: {
          strength: null,
          anthropometry: {
            weight: {
              chartData: {
                labels:[],
                  datasets: [
                  {
                    label: '',
                    backgroundColor: '#286090',
                    data: []
                  }
                ]
              }
            },
            waist_size: {
              chartData: {
                labels:[],
                  datasets: [
                  {
                    label: '',
                    backgroundColor: '#42f49e',
                    data: []
                  }
                ]
              }
            },
            thigh_size: {
              chartData: {
                labels:[],
                  datasets: [
                  {
                    label: '',
                    backgroundColor: '#30f2d1',
                    data: []
                  }
                ]
              }
            },
            body_fat_percentage: {
               chartData: {
                labels:[],
                  datasets: [
                  {
                    label: '',
                    backgroundColor: '#d3ea27',
                    data: []
                  }
                ]
              }
            },
            body_fat_mass: {
               chartData: {
                labels:[],
                  datasets: [
                  {
                    label: '',
                    backgroundColor: '#e4f759',
                    data: []
                  }
                ]
              }
            },
           muscle_mass: {
               chartData: {
                labels:[],
                  datasets: [
                  {
                    label: '',
                    backgroundColor: '#ef410b',
                    data: []
                  }
                ]
              }
            },
           muscle_mass_percentage: {
               chartData: {
                labels:[],
                  datasets: [
                  {
                    label: '',
                    backgroundColor: '#f25a2b',
                    data: []
                  }
                ]
              }
            }
          },
          mobility: null,
          endurance: null
          },
          chartData: {
            labels:[],
            datasets: [
              {
                label: 'Training timeline',
                backgroundColor: '#286090',
                data: []
              }
            ]
          }
        }
      },
      props: ['user_id'],
      methods: {
        trainingHistory(){
          let self = this;

          fetch('/api/sessions_from_beginning', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_id: this.user_id})
          }).then(resp => {
            resp.json().then(data => {
              for(let i = 0; i < data.length; i++) {
                let label = data[i][2].toString() + '-' + data[i][3].toString();
                self.chartData.labels.push(label);
                self.chartData.datasets[0].data.push(data[i][1]);
              }
            })
          })
        },
        testHistory(){
          let self = this;

          fetch('/api/test_history',{
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_id: this.user_id})
          }).then(resp => {
            resp.json().then(data => {
              for(let i = 0; i < data.anthropometry.length; i++){
                self.test_history.anthropometry.weight.chartData.datasets[0].label = 'Weight history (kg)';
                self.test_history.anthropometry.weight.chartData.labels.push(data.anthropometry[i].date_done);
                self.test_history.anthropometry.weight.chartData.datasets[0].data.push(data.anthropometry[i].weight);

                self.test_history.anthropometry.waist_size.chartData.datasets[0].label = 'Waist circumference history (cm)';
                self.test_history.anthropometry.waist_size.chartData.labels.push(data.anthropometry[i].date_done);
                self.test_history.anthropometry.waist_size.chartData.datasets[0].data.push(data.anthropometry[i].waist);

                self.test_history.anthropometry.thigh_size.chartData.datasets[0].label = 'Thigh circumference history (cm)';
                self.test_history.anthropometry.thigh_size.chartData.labels.push(data.anthropometry[i].date_done);
                self.test_history.anthropometry.thigh_size.chartData.datasets[0].data.push(data.anthropometry[i].thigh);

                self.test_history.anthropometry.body_fat_percentage.chartData.datasets[0].label = 'Body fat percentage (%)';
                self.test_history.anthropometry.body_fat_percentage.chartData.labels.push(data.anthropometry[i].date_done);
                self.test_history.anthropometry.body_fat_percentage.chartData.datasets[0].data.push(data.anthropometry[i].body_fat_percentage);

                self.test_history.anthropometry.body_fat_mass.chartData.datasets[0].label = 'Body fat mass (kg)';
                self.test_history.anthropometry.body_fat_mass.chartData.labels.push(data.anthropometry[i].date_done);
                self.test_history.anthropometry.body_fat_mass.chartData.datasets[0].data.push(data.anthropometry[i].body_fat_mass);

                self.test_history.anthropometry.muscle_mass.chartData.datasets[0].label = 'Muscle mass (kg)';
                self.test_history.anthropometry.muscle_mass.chartData.labels.push(data.anthropometry[i].date_done);
                self.test_history.anthropometry.muscle_mass.chartData.datasets[0].data.push(data.anthropometry[i].muscle_mass);

                self.test_history.anthropometry.muscle_mass_percentage.chartData.datasets[0].label = 'Muscle mass percentage (%)';
                self.test_history.anthropometry.muscle_mass_percentage.chartData.labels.push(data.anthropometry[i].date_done);
                self.test_history.anthropometry.muscle_mass_percentage.chartData.datasets[0].data.push(data.anthropometry[i].muscle_mass_percentage);
              }

            })
          })
        }
      },
      created(){
        this.trainingHistory();
        this.testHistory();
      }
    }
</script>

<style scoped>
  .calendar-wrapper{
    margin: 1%;
    text-align: center;
    width: 35%;
  }

  .chart-wrapper{
    background: white;
  }

  @media screen and (max-width: 568px){
    .calendar-wrapper{
      width: 100% !important;
    }
  }
</style>
