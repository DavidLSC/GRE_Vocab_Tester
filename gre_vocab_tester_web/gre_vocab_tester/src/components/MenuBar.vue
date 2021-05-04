<template>
  <div class="menu-bar" v-bind:class="{ responsive: menuIsResponsive }">
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
    <a class="icon" v-on:click="rwd_showMenuBar">
      <i class="fas fa-bars"></i>
    </a>
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
      //RWD control
      menuIsResponsive: false,
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
        if (this.menuIsResponsive) {
          this.$emit("rwdDropDownExpand", false);
        }
      } else {
        this.is_userInfo_dropdown_visible = true;
        if (this.menuIsResponsive) {
          this.$emit("rwdDropDownExpand", true);
        }
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

    //RWD
    rwd_showMenuBar: function () {
      if (this.menuIsResponsive) {
        console.log("is   ");
        this.menuIsResponsive = false;
        this.$emit("rwdMenuExpand", false);
      } else {
        console.log("is  not");
        this.menuIsResponsive = true;
        this.$emit("rwdMenuExpand", true);
      }
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
  z-index: 1;
  /* overflow: hidden; */
}

/* #dictionary-menu-button,
#test-menu-button,
#main-menu-button,
#login,
#userName,
.icon  */
.menu-bar a {
  float: left;
  color: #f2f2f2;
  display: block;
  text-align: center;
  padding: 14px 16px;
  font-size: 17px;
  cursor: pointer;
}

.menu-bar a:hover {
  background-color: #41b883;
}

.menu-bar a.icon {
  display: none;
}

#login,
#userName {
  float: right;
}

.userInfo {
  float: right;
  overflow: hidden;
}

.userLoginDropDown {
  margin: 51px 0 0 0;
  position: absolute;
  display: block;
  z-index: 1;
  background-color: #404040;
  box-shadow: 0px 0px 16px 8px rgba(0, 0, 0, 0.2);
  /* right: 0; */
}

.userLoginDropDown a {
  float: none;
  color: #f2f2f2;
  padding: 12px 16px;
  display: block;
  text-align: center;
  font-size: 17px;
  /* right: 0; */
}

.userInfo:hover .userLoginDropDown {
  display: block;
}

@media screen and (max-width: 600px) {
  /* #dictionary-menu-button,
  #test-menu-button,
  #login,
  .userInfo  */
  .menu-bar a {
    display: none;
  }

  /* #main-menu-button {
    display: block;
  } */
  .menu-bar a.icon {
    float: left;
    display: block;
  }

  .menu-bar {
    position: absolute;
    overflow: hidden;
  }
}

@media screen and (max-width: 600px) {
  .menu-bar.responsive {
    position: absolute;
    display: flex;
    flex-direction: column;
  }
  .menu-bar.responsive .icon {
    order: -1;
  }
  /* .menu-bar.responsive .icon {
    position: absolute;
    right: 0;
    top: 0;
  } */
  .menu-bar.responsive a {
    float: none;
    display: block;
    text-align: left;
  }

  #login,
  #userName {
    float: none;
  }

  .userLoginDropDown {
    margin: 0;
  }

  .menu-bar.responsive .userInfo {
    float: none;
  }
  .menu-bar.responsive .userLoginDropDown {
    position: relative;
  }
  .menu-bar.responsive .userInfo #userName {
    display: block;
    width: 100%;
    text-align: left;
  }
}
</style>
