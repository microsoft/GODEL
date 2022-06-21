<template>
<div>
    <basic-vue-chat :title="'DialoGLM Interface'" :initial-feed="feed" @newOwnMessage="test" :new-message="message" ref="child"/>
      <b-card class="mt-3" header="Knowledge" style="text-align:left">
          <b-form-textarea
        id="textarea"
        v-model="memory"
        placeholder="Place the grounding information here"
        rows="3"
        max-rows="6"
      ></b-form-textarea>
    </b-card>
</div>
</template>

<style lang="scss">
$primary : red;
$font-weight : 800 ;
@import "@/assets/scss/main.scss";
$primary : red;
$font-weight : 800 ;
</style>


<script>
import moment from 'moment'
import BasicVueChat from 'basic-vue-chat'
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)

const cfeed = [
  
  {
    id: 1,
    author: 'System',
    imageUrl: '',
    contents: 'Welcome to our system. Please chat with the agent in the below window.',
    date: ''
  },
]


export default {
  name: 'chat',
  components: {
    BasicVueChat
  },
  data: function () {
    return {
      message: {
            id: 0,
            author: 'Person',
            imageUrl: '',
            image: '',
            contents: 'hi there',
            date: '16:30'
      },
      feed : cfeed,
      all_data : [],
      memory : ''
    }
  },
  methods : {
      test (message, image, imageUrl) {
        //   alert(message)
      const newOwnMessage = {
        id: 1,
        author : 'Person',
        contents: message,
        image: image,
        imageUrl: imageUrl,
        date: moment().format('HH')
      }
      newOwnMessage
      this.all_data.push(message)
      this.$emit('newOwnMessage', message)
    
    },
  },
mounted() {
      this.$on("newOwnMessage", (p) => {
        p
        axios({
              method: 'POST',
              url: 'http://localhost:8082/generate',
              data: {'msg':this.all_data, 'knowledge':this.memory},
              
          }).then(response => {

              this.all_data.push(response.data.response)

                const newOwnMessage = {
                    id: 1,
                    author : 'Agent',
                    contents: response.data.response,
                    image: null,
                    imageUrl: null,
                    date: moment().format('HH:MM:SS')
                }
              this.message = newOwnMessage
              console.log(response);
          }).catch(function (error) {
              console.log(error);
          });
        })
    }
}
</script>

