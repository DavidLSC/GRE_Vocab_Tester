<template>
  <div
    id="app"
    v-bind:class="{
      'margin-60px': is_app_margin_responsive,
      'margin-260px': is_rwd_menu_expanded,
      'margin-400px': is_rwd_dropdown_expanded,
    }"
  >
    <MenuBar
      v-bind:login_user_data="login_user_data"
      v-on:showTQ="tqVisibility(true)"
      v-on:showHome="homeVisibility(true)"
      v-on:showDict="dictVisibility(true)"
      v-on:showLogin="loginVisibility(true)"
      v-on:logout="logout()"
      v-on:viewProfile="viewUserProfile()"
      v-on:viewPersonalList="viewPersonalList()"
      v-on:rwdDropDownExpand="rwd_appMarginTop('rwdDropDownExpand', $event)"
      v-on:rwdMenuExpand="rwd_appMarginTop('rwdMenuExpand', $event)"
    ></MenuBar>
    <!-- <img alt="Vue logo" src="./assets/logo.png" /> -->
    <span
      class="fa-stack fa-lg logo"
      v-bind:class="{
        'fa-8x': !is_icon_responsive,
        'fa-6x': is_icon_responsive,
      }"
    >
      <i class="fab fa-glide fa-stack-1x logo1"></i>
      <i class="fas fa-square fa-stack-2x logo2"></i>
    </span>
    <div id="appPages">
      <div v-if="is_home_visible">
        <Home />
      </div>
      <div v-if="is_test_visible">
        <TestPage
          v-bind:api_fetched_data="fetchAllUnitData()"
          v-bind:API="API"
          v-bind:login_user_data="login_user_data"
        ></TestPage>
      </div>
      <div v-if="is_dict_visible">
        <Dictionary
          v-bind:API="API"
          v-bind:login_user_data="login_user_data"
        ></Dictionary>
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
        v-on:createAccount="createAccount($event)"
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

      //RWD icon
      is_icon_responsive: false,
      //RWD app margin-top
      is_app_margin_responsive: false,
      is_rwd_menu_expanded: false,
      is_rwd_dropdown_expanded: false,
    };
  },
  created() {
    const API = new API_Connector("https://gre-vocab-flask-app.herokuapp.com/");
    this.API = API;

    //RWD
    if (window.matchMedia("(max-width:400px)").matches) {
      this.is_icon_responsive = true;
    } else {
      this.is_icon_responsive = false;
    }
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
              userId: json.userId,
              userFile: json.userFile,
            };
          } else {
            this.$refs.LoginPage.loginError();
          }
        });
    },

    createAccount: function (value) {
      this.API.createAccount(value)
        .then((resp) => resp.json())
        .then((json) => {
          console.log(json.message);
        });
    },

    logout: function () {
      this.login_user_data = null;
      this.userProfileVisibility(false);
      this.homeVisibility(true);
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

    //RWD
    rwd_appMarginTop: function (mode, value) {
      console.log(mode, value);
      if (mode == "rwdMenuExpand") {
        if (value) {
          console.log("xx");
          this.is_rwd_menu_expanded = true;
        } else {
          console.log("yy");
          this.is_rwd_menu_expanded = false;
        }
      } else if (mode == "rwdDropDownExpand") {
        if (value) {
          this.is_rwd_dropdown_expanded = true;
        } else {
          this.is_rwd_dropdown_expanded = false;
        }
      }
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
  height: 100%;
  margin-top: 60px;
}

#appPages {
  height: 100%;
  padding: 20px 20px 20px 20px;
  margin: 0 10% 0 10%;
  background-color: #d7dae1;
  border-style: none;
  border-radius: 20px;
}

.logo1 {
  color: #41b883;
  z-index: 1;
}

.html,
body {
  height: auto;
}

html {
  background-color: #4f7b95;
}

@media screen and (max-width: 600px) {
  #app.margin-60px {
    margin-top: 60px;
  }

  #app.margin-260px {
    margin-top: 260px;
  }

  #app.margin-400px {
    margin-top: 400px;
  }
}
</style>
