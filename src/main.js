import Vue from 'vue'
import Komponenta from './Komponenta'
import NewTraining from './NewTraining'

if (document.getElementById('training-app')) {
  new Vue({
    el: '#training-app',
    components: {
      'komponenta': Komponenta,
      'new-training': NewTraining
    }
});
}


