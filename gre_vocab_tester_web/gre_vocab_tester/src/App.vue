<template>
  <div id="app">
    <MenuBar
      v-on:showTQ="tqVisibility(true)"
      v-on:showHome="homeVisibility(true)"
      v-on:showDict="dictVisibility(true)"
    ></MenuBar>
    <img alt="Vue logo" src="./assets/logo.png" />
    <div id="appPages">
      <div v-if="is_home_visible">
        <Home />
      </div>
      <div v-if="is_test_visible">
        <TestPage
          v-bind:api_fetched_data="fetchAllUnitData()"
          v-bind:API="API"
        ></TestPage>
      </div>
      <div v-if="is_dict_visible">
        <Dictionary v-bind:API="API"></Dictionary>
      </div>
    </div>
  </div>
</template>

<script>
//API_Data
import API_Connector from "./API_Data/API_Connector.js";

//Components
import TestPage from "./components/TestPage.vue";
// import TestQuestion from "./components/TestQuestion.vue";
import MenuBar from "./components/MenuBar.vue";
import Home from "./components/Home.vue";
import Dictionary from "./components/Dictionary.vue";

//const API = new API_Connector("http://localhost:5000");

export default {
  name: "App",
  components: {
    TestPage,
    // TestQuestion,
    MenuBar,
    Home,
    Dictionary,
  },
  data() {
    return {
      is_home_visible: true,
      is_test_visible: false,
      is_dict_visible: false,
      API: null,
    };
  },
  created() {
    const API = new API_Connector("https://gre-vocab-flask-app.herokuapp.com/");
    this.API = API;
  },
  methods: {
    tqVisibility: function (is_test_visible) {
      this.is_test_visible = is_test_visible;
      if (is_test_visible) {
        this.is_home_visible = false;
        this.is_dict_visible = false;
      }
    },
    homeVisibility: function (is_home_visible) {
      this.is_home_visible = is_home_visible;
      if (is_home_visible) {
        this.is_test_visible = false;
        this.is_dict_visible = false;
      }
    },
    dictVisibility: function (is_dict_visible) {
      this.is_dict_visible = is_dict_visible;
      if (is_dict_visible) {
        this.is_test_visible = false;
        this.is_home_visible = false;
      }
    },
    // this passes a promise to the TestQuestion
    //TODO: try to pass this under two level
    fetchAllTestData: function () {
      return this.API.getAllTest();
      //return fetch("http://localhost:5000/getAllTest");
    },

    // this passes a promise to the TestPage for allUnits
    fetchAllUnitData: function () {
      return this.API.getAllUnits();
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  font-size: 20px;
  color: #2c3e50;
  margin-top: 60px;
  height: 100%;
}

#appPages {
  height: 100%;
  padding: 20px 20px 20px 20px;
  margin: 0 10% 0 10%;
  background-color: #d7dae1;
  border-style: none;
  border-radius: 20px;
}

html,
body {
  height: auto;
}

html {
  background-color: #4f7b95;
}
</style>
