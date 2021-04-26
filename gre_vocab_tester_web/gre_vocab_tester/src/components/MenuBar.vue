<template>
  <div class="menu-bar">
    <span>
      <a id="main-menu-button" v-on:click="$emit('showHome')"> Home </a>
      <a id="test-menu-button" v-on:click="$emit('showTQ')">Test</a>
      <a id="dictionary-menu-button" v-on:click="$emit('showDict')"
        >Dictionary</a
      >
      <a id="login">Login</a>
    </span>
  </div>
</template>

<script>
export default {
  name: "MenuBar",
  props: {
    msg: String,
  },
  data() {
    return { state: "home" };
  },
  methods: {
    homeButttonAction: function () {
      this.state = "home";
      console.log("main button action");
    },
    testMenuButtonAction: function () {
      this.state = "test";
      console.log("testMenuAction");
    },
    dictButtonAction: function () {
      this.state = "dictionary";
      console.log("dictAction");
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
  overflow: hidden;
}

.menu-bar a {
  float: left;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  font-size: 17px;
}

.menu-bar a:hover {
  background-color: #ddd;
}

#login {
  float: right;
}
</style>
