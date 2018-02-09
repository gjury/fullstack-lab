Vue.component('risk-list',{

  props:['risk'],
  template:`<div class="card">
              <div class="card-content">
                <p class="title">{{risk.name}}</p>
                <p class="subtitle">{{risk.description}}</p>
                <footer class="card-footer">
                  <a href="#" v-on:click="riskChosen" class="card-footer-item">View</a>

                </footer>
              </div>
            </div>
  `,
  methods:{
    riskChosen() {
      this.$emit('chosen',this);
    }
  }




});

Vue.component('risk-details',{


  props:['dets'],
  template:`

  <ul>
    <li v-for="(el,index) in dets">
        <h2>  {{ el['name'] }}</h2>
      <template v-if="el['type']=='string'">
          <input class="input is-rounded" type="text" placeholder="Text input" :value="el['value']">
      </template>
      <template v-if="el['type']=='number'">
          <input class="input is-rounded" type="text" placeholder="Text input" :value="el['value']">

      </template>
      <template v-if="el['type']=='date'">
          <input class="input is-rounded" type="text" :id="'pd'+index" :value="el['value']">
          {{showpicker(index,el['value'])}}

      </template>
      <template v-if="el['type']=='enum'">
          <div class="select is-multiple">
            <select multiple :size="el['enumv'].length">
              <option :selected="ev==el['value']" v-for="ev in el['enumv']" :value="ev">{{ev}}</option>
            </select>
          </div>
      </template>
    </li>
  </ul>
  `,
  data:function(){
    return{
      datepicker:{}
    }
  },
  methods:{
    showpicker(p1,p2) {
          this.datepicker['pd'+p1]=p2
    }
},

   updated: function(){
      for (var key in this.datepicker) {
          if (this.datepicker.hasOwnProperty(key)) {
            window.flatpickr('#'+key,{inline:true , defaultDate:this.datepicker[key]});
        }
      }
   }
});

new Vue({
  el:'#app',

  data:{
        risks:[],

        selectedRisk:1,

        selectedRiskDetails:{Value:''},

        debugtext:'',

  },

  mounted: function(){

  // GET /someUrl
  this.$http.get('risks').then(response => {

    this.debugtext=response.body;
    this.risks=(response.body);

  }, response => {
    // error callback
  });


  },

  methods:{
    displayDetails(obj) {
      this.selectedRisk=obj.risk.id;
      this.$http.get('risk/'+this.selectedRisk).then(response => {

        this.debugtext=response.body;
        this.selectedRiskDetails=(response.body);

      }, response => {
        // error callback
      });

    },

  },


})
