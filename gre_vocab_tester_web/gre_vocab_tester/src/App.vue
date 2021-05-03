<template>
  <div id="app">
    <MenuBar
      v-bind:login_user_data="login_user_data"
      v-on:showTQ="tqVisibility(true)"
      v-on:showHome="homeVisibility(true)"
      v-on:showDict="dictVisibility(true)"
      v-on:showLogin="loginVisibility(true)"
      v-on:logout="logout()"
      v-on:viewProfile="viewUserProfile()"
      v-on:viewPersonalList="viewPersonalList()"
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
      <div v-if="is_userProfile_visible">
        <UserProfile
          v-bind:login_user_data="login_user_data"
          v-bind:viewMode="userProfileMode"
        />
      </div>
    </div>
    <div v-if="is_login_visible">
      <LoginPage
        ref="LoginPage"
        v-on:cancel="loginVisibility(false)"
        v-on:submit="loginSubmit($event)"
      />
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
import LoginPage from "./components/LoginPage.vue";
import UserProfile from "./components/UserProfile.vue";

export default {
  name: "App",
  components: {
    TestPage,
    // TestQuestion,
    MenuBar,
    Home,
    Dictionary,
    LoginPage,
    UserProfile,
  },
  data() {
    return {
      is_home_visible: true,
      is_test_visible: false,
      is_dict_visible: false,
      is_login_visible: false,
      is_userProfile_visible: false,
      API: null,
      //login user's data
      login_user_data: null,
      //userProfile data
      userProfileMode: null,
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
        this.is_userProfile_visible = false;
      }
    },
    homeVisibility: function (is_home_visible) {
      this.is_home_visible = is_home_visible;
      if (is_home_visible) {
        this.is_test_visible = false;
        this.is_dict_visible = false;
        this.is_userProfile_visible = false;
      }
    },
    dictVisibility: function (is_dict_visible) {
      this.is_dict_visible = is_dict_visible;
      if (is_dict_visible) {
        this.is_test_visible = false;
        this.is_home_visible = false;
        this.is_userProfile_visible = false;
      }
    },
    loginVisibility: function (is_login_visible) {
      this.is_login_visible = is_login_visible;
    },
    userProfileVisibility: function (is_userProfile_visible) {
      this.is_userProfile_visible = is_userProfile_visible;
      if (is_userProfile_visible) {
        this.is_test_visible = false;
        this.is_home_visible = false;
        this.is_dict_visible = false;
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

    loginSubmit: function (value) {
      this.API.login(value)
        .then((resp) => resp.json())
        .then((json) => {
          if (json.status == "ok") {
            this.loginVisibility(false);
            this.login_user_data = {
              username: value.username,
            };
          } else {
            this.$refs.LoginPage.loginError();
          }
        });
    },

    logout: function () {
      this.login_user_data = null;
    },

    viewUserProfile: function () {
      let userNameData = { username: this.login_user_data.username };
      if (this.login_user_data.email != undefined) {
        this.userProfileMode = "profileInfo";
        this.userProfileVisibility(true);
      } else {
        this.API.getUserInfo(userNameData)
          .then((resp) => resp.json())
          .then((json) => {
            this.userProfileMode = "profileInfo";
            this.userProfileVisibility(true);
            this.login_user_data = json.data;
            console.log(json);
          });
      }
    },
    viewPersonalList: function () {
      this.userProfileMode = "personalList";
      this.userProfileVisibility(true);
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
