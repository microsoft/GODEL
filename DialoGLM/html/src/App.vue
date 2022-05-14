<template>
<b-container id='app'>
  <chat id='appp' />
</b-container>
</template>

<script>
import chat from './components/chat.vue'
import Vue from 'vue'
import { BootstrapVue} from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)
export default {
  name: 'App',
  components: {
    chat
  }
}

window.onload = function() {
  document.getElementsByClassName('window')[0].style.maxWidth = '100%'
  document.getElementsByClassName('window')[0].style.height = '800px'
};

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
