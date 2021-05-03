<template>
  <div class="loginPage">
    <div class="loginForm" v-if="!showLoading" @keyup.enter="loginSubmit">
      <span class="loginError" v-if="isLoginError"
        >The username or password entered was incorrect. Please try again.</span
      >
      <span> Username: </span>
      <input v-model="userName" />
      <span> Password: </span>
      <input v-bind:type="passwordFieldType" v-model="password" />
      <span class="loginButtons">
        <span v-on:click="loginCancel()">Cancel</span>
        <span class="important" v-on:click="loginSubmit()">Login</span>
      </span>
    </div>
    <div class="loading" v-if="showLoading"><p>Loading...</p></div>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  props: {},
  data() {
    return {
      userName: null,
      password: null,
      showLoading: false,
      isLoginError: false,
      passwordFieldType: "password",
    };
  },
  methods: {
    loginError: function () {
      this.isLoginError = true;
      this.showLoading = false;
    },
    loginCancel: function () {
      this.$emit("cancel");
    },
    loginSubmit: function () {
      console.log(this.userName, this.password);
      if (
        !(this.userName == null || this.userName == "") &&
        !(this.password == null || this.password == "")
      ) {
        this.showLoading = true;
        console.log(this.userName, this.password);
        let loginInfo = {
          username: this.userName,
          password: this.password,
        };
        this.$emit("submit", loginInfo);
      } else {
        alert("Please enter your username and password before login");
      }
    },
  },
};
</script>

<style scoped>
.loginPage {
  padding: 15px 15px 15px 15px;
  z-index: 99999;
  position: fixed;
  top: 25%;
  bottom: 25%;
  right: 25%;
  left: 25%;

  background-color: #d7dae1;
  border-style: solid;
  border-width: 2px 5px 5px 2px;
  border-radius: 10px;
}

.loginForm {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.loginForm span:not(.loginButtons) {
  align-self: flex-start;
}

.loginError {
  text-align: left;
  color: red;
}

.loginForm input {
  padding: 5px 0 5px 0;
  font-size: 18px;
}

.loginButtons {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  flex-wrap: wrap;
}

.important {
  border-style: none;
  padding: 8px 10px 8px 10px;
  border-radius: 10px;
  background-color: #4f7b95;
  color: #d7dae1;
}

.important:hover {
  background-color: #3f6277;
}
.important:active {
  background-color: #2f4959;
}

.loginButtons span:not(.important) {
  border-style: none;
  padding: 8px 10px 8px 10px;
  border-radius: 10px;
  background-color: #c1c4ca;
}

.loginButtons span:hover:not(.important) {
  background-color: #acaeb4;
}
.loginButtons span:active:not(.important) {
  background-color: #96989d;
}

.Loading p {
  margin: 25% 25% 25% 25%;
}
</style>
