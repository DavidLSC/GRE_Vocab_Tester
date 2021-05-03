<template>
  <div class="userProfile">
    <h3>{{ "Welcome back " + login_user_data.username }}</h3>
    <div v-if="viewMode == 'profileInfo'" class="profileInfo">
      <span id="username">{{ "username: " + login_user_data.username }}</span>
      <span id="email">{{ "email: " + login_user_data.email }}</span>
      <span>{{ "id: " + login_user_data.userId }}</span>
      <span>{{ "isAdmin :" + login_user_data.isAdmin }}</span>
    </div>
    <div v-if="viewMode == 'personalList'" class="personalList"></div>
  </div>
</template>

<script>
export default {
  name: "UserProfile",
  props: {
    login_user_data: Object,
    viewMode: String,
  },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
.userProfile {
  text-align: left;
}

.profileInfo {
  display: flex;
  flex-direction: column;
  justify-content: stretch;
  align-items: flex-start;
}
</style>
