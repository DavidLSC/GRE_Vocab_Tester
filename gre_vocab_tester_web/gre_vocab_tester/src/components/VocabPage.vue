<template>
  <div class="vocabPage">
    <div v-if="vocabPageLoading">Loading...</div>
    <div v-else>
      <a class="goBackButton" v-on:click="goBackButtonAction()"
        >&larr; Go Back</a
      >
      <h1>{{ selectedVocab.text }}</h1>
      <span>[{{ selectedVocab.vocabRoot }}]</span>
      <span>{{ selectedVocab.definition }}</span>
      <span>Importancy: {{ selectedVocab.importancy }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "VocabPage",
  props: {
    root: String,
    vocabDataPromise: Promise,
    vocabData: Object,
  },
  data() {
    return {
      selectedVocab: {},
      vocabPageLoading: false,
    };
  },
  created() {
    this.vocabPageLoading = true;
    if (this.vocabData) {
      this.vocabPageLoading = false;
      this.selectedVocab = this.vocabData;
    } else {
      this.vocabDataPromise
        .then((resp) => resp.json())
        .then((json) => {
          this.vocabPageLoading = false;
          if (json.status == "ok") {
            this.selectedVocab = json;
          } else {
            alert(json.message);
          }
        });
    }
  },
  methods: {
    goBackButtonAction: function () {
      console.log("emit event");
      this.$emit("goBack");
      // TODO: this.$emit() a return event for parents to handle visibility
    },
  },
};
</script>

<style scoped>
.vocabPage div {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.goBackButton {
  border-style: none;
  padding: 8px 10px 8px 10px;
  border-radius: 10px;
  background-color: #c1c4ca;
  align-self: flex-start;
}
.goBackButton:hover {
  background-color: #acaeb4;
}
.goBackButton:active {
  background-color: #96989d;
}
</style>