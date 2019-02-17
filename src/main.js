import Vue from 'vue'
import NewTraining from './NewTraining'
import DoTraining from './DoTraining'
import Moment from 'vue-moment'
import VModal from 'vue-js-modal'
import Statistics from './Statistics'
import Tests from './Tests'

// plugins
Vue.use(VModal, { dynamic: true, injectModalsContainer: true });
Vue.use(Moment);

if (document.getElementById('training-app')) {
  new Vue({
    el: '#training-app',
    components: {
      'new-training': NewTraining,
      'do-training': DoTraining,
      'statistics': Statistics,
      'tests': Tests
    }
});
}


