<template>
  <div id="ok-modal">
    <p>{{name}}, thank you for submitting the training!</p>
    <div @click="$emit('close')">
      <p style="margin-bottom: 2px;">Close</p>
    </div>
  </div>
</template>

<script>
    export default {
      name: "OkModal",
      props: ['name']
    }
</script>

<style scoped>
  #ok-modal{
    text-align: center;
  }

  #ok-modal p{
    padding: 13px;
  }

  #ok-modal div{
    border-top: 1px solid #eeee;
    cursor: pointer;
  }

  #ok-modal div:hover{
    background: #eeee;
    color: #646566;
  }
</style>
