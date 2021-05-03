<template>
  <div>
    <div class="vocabPageLoading" v-if="vocabPageLoading">
      <p>Loading</p>
      <i class="fas fa-spinner fa-spin"></i>
    </div>
    <div v-else class="vocabPage">
      <a class="goBackButton" v-on:click="goBackButtonAction()">
        <i class="fas fa-arrow-left"> </i>
        Go Back
      </a>
      <span class="vocabText">
        <h1>{{ selectedVocab.text }}</h1>
        <i
          class="far fa-star notAdded"
          v-if="!isInList"
          v-on:click="modifyPersonalList"
        ></i>
        <i
          class="fas fa-star added"
          v-if="isInList"
          v-on:click="modifyPersonalList"
        ></i>
      </span>
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
      isInList: false,
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
    },
    //TODO: need to think should this method be in vocab
    modifyPersonalList: function () {
      let add = false;
      if (this.isInList) {
        this.changeIsInList(false);
      } else {
        this.changeIsInList(true);
        add = true;
      }
      let vocabData = {
        text: this.selectedVocab.text,
        add: add,
      };
      this.$emit("modifyPersonalList", vocabData);
    },
    changeIsInList: function (bool) {
      this.isInList = bool;
    },
  },
};
</script>

<style scoped>
.vocabPageLoading {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.vocabPage {
  width: 100%;
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

.vocabText {
  display: flex;
  flex-direction: row;
  align-items: baseline;
  flex-wrap: wrap;
}
.vocabText h1 {
  margin: 0 20px 0 0;
}

.vocabText i:hover {
  color: #4c6ef5;
}

.added {
  color: #4c6ef5;
}
</style>