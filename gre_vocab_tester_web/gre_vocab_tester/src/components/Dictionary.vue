<template>
  <div class="dictionary">
    <div class="searchPage" v-if="is_search_visible">
      <h3>Please enter a word</h3>
      <input v-model="userInput" placeholder="Enter the word here" />
      <span class="sortingOptions">
        Sort By
        <select v-model="sortingMode">
          <option disabled value="">Sort Vocabularies By</option>
          <option value="alphabetOrder">Alphabetical Order</option>
          <option value="unitOrder">Unit</option>
        </select>
      </span>
      <div class="result">
        <span
          v-for="(vocab, index) in showedVocab"
          v-bind:key="index"
          v-on:click="showVocab(vocab)"
        >
          {{ vocab }}
        </span>
      </div>
      <a id="viewSearchHistory" v-on:click="showHistoryPage()">View History</a>
    </div>
    <div class="historyPage" v-if="is_history_visible">
      <a class="goBackButton" v-on:click="goBackButtonAction()"
        >&larr; Go Back</a
      >
      <h3>Search History</h3>
      <span
        v-for="{ word, id } in history.slice().reverse()"
        v-bind:key="id"
        v-on:click="showVocab(word)"
      >
        {{ word }}
      </span>
    </div>
    <div v-if="is_vocab_page_visible">
      <VocabPage
        v-bind:vocabDataPromise="vocabPageData"
        v-on:goBack="goBackButtonAction()"
      ></VocabPage>
    </div>
  </div>
</template>

<script>
import VocabPage from "./VocabPage";

export default {
  name: "Dictionary",
  components: {
    VocabPage,
  },
  props: {
    API: Object,
  },
  data() {
    return {
      sortingMode: "",
      userInput: "",
      allVocab: [],
      showedVocab: [],
      sortedVocab: [],
      history: [],
      selectedVocab: {},
      //visiblity control
      is_search_visible: true,
      is_vocab_page_visible: false,
      is_history_visible: false,
      go_back_parent: null,

      //vocabPageData
      vocabPageData: null,
    };
  },
  created() {
    this.API.getAllVocabText()
      .then((resp) => resp.json())
      .then((json) => {
        this.allVocab = json;
        this.showedVocab = json;
      });
  },
  watch: {
    userInput: function (input) {
      this.userInputAction(input);
    },
    sortingMode: function (mode) {
      if (mode == "alphabetOrder") {
        this.showedVocab = [];
        let a = 97;
        let alphbetMap = {};
        for (let i = 0; i < 26; i++) {
          alphbetMap[String.fromCharCode(a + i)] = [];
        }
        // allocate vocab by it's starting letter
        for (let i = 0; i < this.allVocab.length; i++) {
          let firstLetter = this.allVocab[i].charAt(0);
          alphbetMap[firstLetter].push(this.allVocab[i]);
        }
        this.sortedVocab = [];
        for (let i = 0; i < 26; i++) {
          let vocabArr = alphbetMap[String.fromCharCode(a + i)];
          this.sortVocab(vocabArr);
          for (let j in vocabArr) {
            this.showedVocab.push(vocabArr[j]);
            this.sortedVocab.push(vocabArr[j]);
          }
        }
      } else if (mode == "unitOrder") {
        this.showedVocab = [];
        for (let i in this.allVocab) {
          this.showedVocab.push(this.allVocab[i]);
        }
      }
      // invoke the search action after sorting
      this.userInputAction(this.userInput);
    },
  },
  methods: {
    addToHistory: function (word) {
      this.history.push({ word: word, id: null });
      if (this.history.length > 5) {
        this.history.shift();
      }
      for (let i in this.history) {
        this.history[i].id = i;
      }
    },
    showVocab: function (vocabText) {
      if (this.is_history_visible) {
        this.go_back_parent = "historyPage";
      } else {
        this.go_back_parent = "searchPage";
        this.addToHistory(vocabText);
      }
      this.is_search_visible = false;
      this.is_history_visible = false;
      this.is_vocab_page_visible = true;
      this.vocabPageData = this.API.getVocabByText(vocabText);
    },
    goBackButtonAction: function () {
      console.log(this.go_back_parent);
      if (this.go_back_parent == "historyPage") {
        this.showHistoryPage();
      } else if (this.go_back_parent == "searchPage") {
        this.showSearchPage();
      }
    },
    showSearchPage: function () {
      this.is_search_visible = true;
      this.is_vocab_page_visible = false;
      this.is_history_visible = false;
    },
    showHistoryPage: function () {
      this.is_search_visible = false;
      this.is_vocab_page_visible = false;
      this.is_history_visible = true;
      this.go_back_parent = "searchPage";
    },

    sortVocab: function (vocabList) {
      for (let i in vocabList) {
        for (let j = 0; j < vocabList.length - i - 1; j++) {
          try {
            let result = vocabList[j].localeCompare(vocabList[j + 1]);
            if (result == 1) {
              let temp = vocabList[j];
              vocabList[j] = vocabList[j + 1];
              vocabList[j + 1] = temp;
            }
          } catch (err) {
            console.log(err);
          }
        }
      }
    },

    //TODO: if input include none letter word need to handle it
    userInputAction: function (input) {
      this.showedVocab = [];
      let re = RegExp("^" + input, "g");
      if (this.sortingMode == "alphabetOrder") {
        for (let i = 0; i < this.sortedVocab.length; i++) {
          let match = this.sortedVocab[i].search(re);
          if (match != -1) {
            this.showedVocab.push(this.sortedVocab[i]);
          }
        }
      } else {
        for (let i = 0; i < this.allVocab.length; i++) {
          let match = this.allVocab[i].search(re);
          if (match != -1) {
            this.showedVocab.push(this.allVocab[i]);
          }
        }
      }
    },
  },
};
</script>

<style scoped>
.searchPage {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}

.searchPage a {
  border-style: none;
  border-radius: 10px;
  background-color: #c1c4ca;
  margin: 10px 25vw 10px 25vw;
  padding: 10px 10px 10px 10px;
}

.searchPage input {
  text-align: center;
  padding: 5px 0px 5px 0px;
  margin: 1vh 0 1vh 0;
  /* width: 25%; */
  align-self: stretch;
  border-radius: 5px;
  font-size: 18px;
}

.sortingOptions {
  align-self: flex-end;
  right: 0%;
  font-size: 15px;
}

.sortingOptions select {
  right: auto;
  padding: 3px 3px 3px 5px;
  margin: 0 0 0 0;
  border-radius: 5px;
}

.result {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  height: 50vh;
  overflow-y: scroll;
  width: 100%;
  border-radius: 10px;
  padding: 5px 5px 5px 5px;
  margin: 1vh 0 2vh 0;
}

.historyPage {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  width: 100%;
  border-radius: 10px;
  padding: 5px 5px 5px 5px;
}

.result span,
.historyPage span {
  padding: 1px 0 1px 0;
  border-style: none;
  border-radius: 10px;
  background-color: #c1c4ca;
  margin: 5px 0 0 0;
}

.result span:hover,
.historyPage span:hover {
  background-color: #acaeb4;
}

.result span:active,
.historyPage span:active {
  background-color: #96989d;
}

.vocabPage {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  font-size: 22px;
}
.vocabPage span {
  margin: 0px 0px 10px 0px;
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