<template>
  <div id="img-desc-modal">
    <div>
      <h4>{{test.name}}</h4>
    </div>
    <hr>
    <div class="test-description">
      {{test.desc}}
    </div>
    <hr>
    <div class="img-wrapper">
      <img :src="test.img" alt="">
    </div>
    <hr>
    <div @click="$emit('close')">
      <p class="close-modal">Close</p>
    </div>
  </div>
</template>

<script>
    export default {
      name: "ImgDesc",
      data(){
        return{

        }
      },
      props:['test']
    }
</script>

<style scoped>
  #img-desc-modal{
    color: #337ab7;
    text-align: justify;
    text-align-last: center;
  }

  #img-desc-modal img{
    height: 100%;
    width: auto;
  }

  .close-modal{
    background: #337ab7;
    color: white;
    cursor: pointer;
    margin-bottom: 0;
    padding: 7px;
  }

  .close-modal:active{
    background: #2b5eaf;
  }

  .test-description{
    padding: 5px;
  }

  .img-wrapper{
    height: 200px;
    margin: 0 auto;
  }

</style>
