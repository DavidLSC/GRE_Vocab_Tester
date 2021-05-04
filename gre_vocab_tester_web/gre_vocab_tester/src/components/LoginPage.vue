<template>
  <div class="loginPage">
    <div
      class="loginForm"
      v-if="is_login_form_visible"
      @keyup.enter="loginSubmit"
    >
      <span class="loginError" v-if="isLoginError"
        >The username or password entered was incorrect. Please try again.</span
      >
      <span> Username: </span>
      <input v-model="userName" />
      <span> Password: </span>
      <input v-bind:type="passwordFieldType" v-model="password" />
      <a
        style="
          font-size: 15px;
          text-decoration: underline;
          cursor: pointer;
          align-self: flex-start;
        "
        v-on:click="viewCreateAccountPage"
        >New? Create a free account</a
      >
      <span class="loginButtons">
        <span v-on:click="loginCancel()">Cancel</span>
        <span class="important" v-on:click="loginSubmit()">Login</span>
      </span>
    </div>
    <div v-if="is_create_account_visible" class="accountCreateForm">
      <span>Create a new account</span>
      <span>Username:</span>
      <span v-if="createUsernameError" style="color: red; font-size: 15px"
        >Need to be longer then 8 letters</span
      >
      <input v-model="createUsername" />
      <span>Password:</span>
      <span v-if="createPasswordError" style="color: red; font-size: 15px"
        >Need to be longer then 8 letters</span
      >
      <input v-model="createPassword" />
      <span>Email:</span>
      <span v-if="createEmailError" style="color: red; font-size: 15px"
        >Please enter the correct email form.</span
      >
      <input v-model="createEmail" />
      <span class="loginButtons">
        <span v-on:click="loginCancel()">Cancel</span>
        <span class="important" v-on:click="createAccount()">Create</span>
      </span>
    </div>
    <div v-if="is_congrat_visible">
      <span>Congratulation your account has been created</span>
      <span class="loginButtons">
        <span v-on:click="returnToLoginPage">Go to login page</span>
      </span>
    </div>
    <div class="loading" v-if="showLoading">
      <p>Loading</p>
      <i class="fas fa-spinner fa-spin"></i>
    </div>
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
      is_login_form_visible: true,
      is_create_account_visible: false,
      is_congrat_visible: false,
      isLoginError: false,

      passwordFieldType: "password",
      createUsername: null,
      createPassword: null,
      createEmail: null,
      createEmailError: false,
      createUsernameError: false,
      createPasswordError: false,
    };
  },
  methods: {
    loginError: function () {
      this.isLoginError = true;
      this.showLoading = false;
      this.is_login_form_visible = true;
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
        this.is_login_form_visible = false;
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
    viewCreateAccountPage: function () {
      console.log("create");
      this.is_login_form_visible = false;
      this.is_create_account_visible = true;
    },
    createAccount: function () {
      console.log(
        "create Account submission",
        this.createUsername,
        this.createPassword,
        this.createEmail
      );
      if (this.createUsername && this.createPassword && this.createEmail) {
        //check if input value is valid
        this.checkInputValid();
        if (
          this.createEmailError != true &&
          this.createPasswordError != true &&
          this.createUsernameError != true
        ) {
          let createAccountData = {
            username: this.createUsername,
            password: this.createPassword,
            email: this.createEmail,
          };
          this.$emit("createAccount", createAccountData);
          this.is_create_account_visible = false;
          this.is_congrat_visible = true;
        }
      } else {
        alert("Please enter each part to create account");
      }
    },
    checkInputValid: function () {
      let emailCheck = /^\w+@\w+[.]\w+$/;
      if (this.createEmail.search(emailCheck) == -1) {
        this.createEmailError = true;
      } else {
        this.createEmailError = false;
      }
      this.createUsername.length > 7
        ? (this.createUsernameError = false)
        : (this.createUsernameError = true);
      this.createPassword.length > 7
        ? (this.createPasswordError = false)
        : (this.createPasswordError = true);
    },
    returnToLoginPage: function () {
      this.is_login_form_visible = true;
      this.is_congrat_visible = false;
    },
  },
};
</script>

<style scoped>
/* TODO: responsive needed or the content extend all the time*/

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

.loginPage div {
  height: 100%;
}

.loginForm,
.accountCreateForm {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
}

.loginForm span:not(.loginButtons),
.accountCreateForm span:not(.loginButtons) {
  align-self: flex-start;
}

.loginError {
  text-align: left;
  color: red;
}

.loginForm input,
.accountCreateForm input {
  padding: 5px 0 5px 5px;
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
