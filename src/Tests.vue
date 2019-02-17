<template>
    <div id="tests">
       <modals-container>
       </modals-container>
      <div class="col-md-8 col-md-offset-2 col-sm-12">
        <div class="nav-wrapper">
          <div @click="changeCategory('anthropometry')" class="nav-button btn btn-primary">Anthropometry</div>
          <div @click="changeCategory('strength')" class="nav-button btn btn-success btn btn-success">Strength</div>
          <div @click="changeCategory('endurance')" class="nav-button btn btn-info">Endurance</div>
          <div @click="changeCategory('mobility')" class="nav-button btn btn-warning">Mobility</div>
        </div>
        <div class="tests-wrapper" v-if="category === 'anthropometry'">
          <div class="row">
           <div class="col-md-12">
             <div>
               <h3>Weight & body circumferences</h3>
             </div>
             <div class="test-name-wrapper">
               <div class="test-name">
                <div @click="showModal(anthropometry.weight, 340, 400)">
                 {{anthropometry.weight.name}} <i class="glyphicon glyphicon-info-sign test-info"></i>
                </div>
                 <input v-model="anthropometryResults.weight" class="form-control input-result" type="text" :placeholder="'(' + anthropometry.weight.unit + ')'">
               </div>

               <div class="test-name">
                <div @click="showModal(anthropometry.waist, 340, 400)">
                 {{anthropometry.waist.name}} <i class="glyphicon glyphicon-info-sign test-info"></i>
                </div>
                 <input v-model="anthropometryResults.waist" class="form-control input-result" type="text" :placeholder="'(' + anthropometry.waist.unit + ')'">
               </div>

               <div class="test-name">
                <div @click="showModal(anthropometry.thigh, 340, 400)">
                 {{anthropometry.thigh.name}} <i class="glyphicon glyphicon-info-sign test-info"></i>
                </div>
                 <input v-model="anthropometryResults.thigh" class="form-control input-result" type="text" :placeholder="'(' + anthropometry.thigh.unit + ')'">
               </div>
             </div>
            </div>
          </div>
          <hr>
          <div class="row">
            <div class="col-md-12">
             <div>
               <h3>Body composition</h3>
             </div>
             <div class="test-name-wrapper">
               <div class="test-name test-body">
                 <div @click="showModal(anthropometry.body_fat_percentage, 340, 400)">
                  {{anthropometry.body_fat_percentage.name}} <i class="glyphicon glyphicon-info-sign test-info"></i>
                </div>
                 <input v-model="anthropometryResults.body_fat_percentage" class="form-control input-result" type="text" :placeholder="'(' + anthropometry.body_fat_percentage.unit + ')'">
               </div>

               <div class="test-name test-body">
                 <div @click="showModal(anthropometry.body_fat_mass, 340, 400)">
                  {{anthropometry.body_fat_mass.name}} <i class="glyphicon glyphicon-info-sign test-info"></i>
                </div>
                 <input v-model="anthropometryResults.body_fat_mass" class="form-control input-result" type="text" :placeholder="'(' + anthropometry.body_fat_mass.unit + ')'">
               </div>

               <div class="test-name test-body">
                 <div @click="showModal(anthropometry.muscle_mass_percentage, 340, 400)">
                  {{anthropometry.muscle_mass_percentage.name}} <i class="glyphicon glyphicon-info-sign test-info"></i>
                </div>
                 <input v-model="anthropometryResults.muscle_mass_percentage" class="form-control input-result" type="text" :placeholder="'(' + anthropometry.muscle_mass_percentage.unit + ')'">
               </div>

               <div class="test-name test-body">
                 <div @click="showModal(anthropometry.muscle_mass, 340, 400)">
                  {{anthropometry.muscle_mass.name}} <i class="glyphicon glyphicon-info-sign test-info"></i>
                </div>
                <input v-model="anthropometryResults.muscle_mass" class="form-control input-result" type="text" :placeholder="'(' + anthropometry.muscle_mass.unit + ')'">
               </div>
            </div>
          </div>
          </div>
          <div class="row" style="margin: 2% 0;">
            <div>
              <button @click="submitResults" class="btn btn-primary">Submit results</button>
            </div>
          </div>
        </div>
      </div>
      <div class="clearfix"></div>
    </div>
</template>

<script>
  import ImgDescModal from './modals/ImgDescModal'

    export default {
      name: "Tests",
      data(){
        return {
          category: 'anthropometry',
          testId: 1,
          tests: null,
          anthropometryResults: {
            weight: null,
            waist: null,
            thigh: null,
            body_fat_percentage: null,
            body_fat_mass: null,
            muscle_mass_percentage: null,
            muscle_mass: null
          },
          anthropometry: {
            weight: {
              name: 'Weight scale test',
              desc: 'For the best and most accurate results, weight scale test should be performed in the morning, on empty stomach, in the underwear.',
              img: '/static/images/tests/weight_scale.jpg',
              unit: 'kg'
            },
            waist: {
              name: 'Waist circumference test',
              desc: 'Waist circumference test should be performed in standing position, with measuring tape in the height of the belly button. Be sure to apply right pressure, and to keep measuring tape horizontal and not inclined.',
              img: '/static/images/tests/waist-circumference.jpg',
              unit: 'cm'
            },
            thigh: {
              name: 'Thigh circumference test',
              desc: 'Thigh circumference test should be performed in standing position, with measuring tape in the height of the upper third of the thigh. No clothing should be present. Be sure to apply right pressure, and to keep measuring tape horizontal and not inclined.',
              img: '/static/images/tests/thigh.png',
              unit: 'cm'
            },
            body_fat_percentage: {
              name: 'Body fat percentage',
              desc: '',
              img: '',
              unit: '%'
            },
            body_fat_mass: {
              name: 'Body fat mass',
              desc: '',
              img: '',
              unit: 'kg'
            },
            muscle_mass_percentage: {
              name: 'Muscle mass percentage',
              desc: '',
              img: '',
              unit: '%'
            },
            muscle_mass: {
              name: 'Muscle mass',
              desc: '',
              img: '',
              unit: 'kg'
            }
          }
        }
      },
      props: ['user'],
      methods: {
        changeCategory(param){
          this.category = param;
        },
        showModal(test, width, height){
          this.$modal.show(ImgDescModal, {
            test: test
          },
            {
              width: width,
              height: 'auto'
            })
        },
        submitResults(){
          let self = this;

          switch (this.category){
            case 'anthropometry':
              if (this.checkValues()) {
                  fetch('/tests/post_results', {
                     method: 'POST',
                      headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                      },
                      body: JSON.stringify({
                        results: self.anthropometryResults,
                        user_id: self.user,
                        type: 'anthropometry'
                      })
                  }).then(resp => {
                    resp.json().then(data => {
                      console.log(data);
                    })
                  })
              }
          }
        },
        checkValues(type){
          return true;
        }
      }
    }
</script>

<style>
  #tests{
    text-align: center;
  }

  #tests h3{
    color: #337ab7;
  }

  .tests-wrapper{
    background: white;
    border: 1px solid #eeee;
    border-radius: 7px;
    box-shadow: 5px 5px #eeee;
    margin-top: 2%;
  }

  .test-name-wrapper{
    margin-top: 2%;
  }

  .test-name{
    background: #337ab7;
    color: white;
    display: inline-block;
    font-weight: bold;
    cursor: pointer;
    margin: 1% 0.5%;
    padding: 8px;
    position: relative;
    width: 31.5%;
  }

  .test-body{
    width: 23.5%;
  }

  .test-info{
    position: absolute;
    right: 12px;
    top: 10px;
  }

  .input-result{
    margin-top: 2%;
  }

  @media screen and (max-width: 568px){
    #tests{
      font-size: 0.95em;
    }

    .nav-button{
      font-size: 0.9em;
    }
    .test-name{
      display: block;
      width: 100%;
    }
  }

</style>
