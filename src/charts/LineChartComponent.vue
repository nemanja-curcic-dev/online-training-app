<script>
  import { Line, mixins } from 'vue-chartjs'

  export default {
    name: "BarChartComponent",
    extends: Line,
    mixins: [mixins.reactiveProp],
    mounted(){
      this.renderChart(this.chartData,
      {
        legend: {
          labels:{
            fontSize: 14
          }
        },
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              display: false
            }
          }],
          xAxes: [ {
            gridLines: {
              display: true
            },
          }]
        },
        responsive: true,
        maintainAspectRatio: false,
        position: 'relative',
        showInlineValues: true
      })
    }
  }
</script>

<style scoped>

</style>

