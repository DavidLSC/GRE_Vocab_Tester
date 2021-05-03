<template>
  <div class="menu-bar">
    <a id="main-menu-button" v-on:click="homeButttonAction()">
      <i class="fas fa-home"></i>
      Home
    </a>
    <a id="test-menu-button" v-on:click="testMenuButtonAction()">
      <i class="fas fa-clipboard-list"></i>
      Test
    </a>
    <a id="dictionary-menu-button" v-on:click="dictButtonAction()">
      <i class="fas fa-book"></i>
      Dictionary
    </a>
    <a id="login" v-if="!isUserLogin" v-on:click="loginButtonAction()">Login</a>
    <div class="userInfo" v-if="isUserLogin">
      <a id="userName" v-on:click="dropDownMenuVisbility">{{
        "Hi, " + login_user_data.username
      }}</a>
      <div class="userLoginDropDown" v-if="is_userInfo_dropdown_visible">
        <a v-on:click="viewProfile">Profile</a>
        <a v-on:click="viewPersonalList">Personal List</a>
        <a v-on:click="logOut">Logout</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MenuBar",
  props: {
    login_user_data: Object,
  },
  data() {
    return {
      isUserLogin: false,
      is_userInfo_dropdown_visible: false,
    };
  },
  watch: {
    login_user_data: function (login_user_data) {
      if (login_user_data) {
        this.isUserLogin = true;
      } else {
        this.isUserLogin = false;
      }
      console.log(login_user_data);
    },
  },
  methods: {
    homeButttonAction: function () {
      this.$emit("showHome");
    },
    testMenuButtonAction: function () {
      this.$emit("showTQ");
    },
    dictButtonAction: function () {
      this.$emit("showDict");
    },
    loginButtonAction: function () {
      this.$emit("showLogin");
    },
    dropDownMenuVisbility: function () {
      if (this.is_userInfo_dropdown_visible) {
        this.is_userInfo_dropdown_visible = false;
      } else {
        this.is_userInfo_dropdown_visible = true;
      }
    },
    //TODO: make a userPage for Profile and Personal List
    viewProfile: function () {
      this.$emit("viewProfile");
      this.dropDownMenuVisbility(false);
    },
    viewPersonalList: function () {
      this.$emit("viewPersonalList");
      this.dropDownMenuVisbility(false);
    },
    logOut: function () {
      this.dropDownMenuVisbility(false);
      this.$emit("logout");
    },
  },
};
</script>


<style scoped>
.menu-bar {
  position: absolute;
  right: 0px;
  top: 0px;
  left: 0px;
  background-color: #333;
  /* overflow: hidden; */
}

.menu-bar a:not(.userLoginDropDown a) {
  float: left;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  font-size: 17px;
  cursor: pointer;
}

.menu-bar a:hover {
  background-color: #41b883;
}

#login,
#userName {
  float: right;
}

.userInfo {
  float: right;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.userLoginDropDown {
  margin: 51px 0 0 0;
  position: absolute;
  display: block;
  z-index: 1;
  background-color: #333;
  /* min-width: 160px; */
}

.userLoginDropDown a {
  color: #f2f2f2;
  padding: 12px 16px;
  display: block;
  text-align: center;
  float: none;
  font-size: 17px;
}

.userInfo:hover .userLoginDropDown {
  display: block;
}
</style>
