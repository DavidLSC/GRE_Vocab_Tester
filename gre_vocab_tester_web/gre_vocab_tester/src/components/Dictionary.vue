<template>
  <div class="dictionary">
    <div class="searchPage" v-if="is_search_visible">
      <span>Please enter a word</span>
      <p>
        <input v-model="userInput" placeholder="Enter the word here" />
      </p>
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
      <a class="goBackButton" v-on:click="showSearchPage()">&larr; Go Back</a>
      <h3>Search History</h3>
      <span
        v-for="{ word, id } in history.slice().reverse()"
        v-bind:key="id"
        v-on:click="showVocab(word, true)"
      >
        {{ word }}
      </span>
    </div>
    <div class="vocabPage" v-if="is_vocab_page_visible">
      <a class="goBackButton" v-on:click="showSearchPage()">&larr; Go Back</a>
      <h1>{{ selectedVocab.text }}</h1>
      <span>[{{ selectedVocab.vocabRoot }}]</span>
      <span>{{ selectedVocab.definition }}</span>
      <span>Importancy: {{ selectedVocab.importancy }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dictionary",
  props: {
    API: Object,
  },
  data() {
    return {
      userInput: null,
      allVocab: [],
      showedVocab: [],
      history: [],
      selectedVocab: {},
      is_search_visible: true,
      is_vocab_page_visible: false,
      is_history_visible: false,
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
      this.showedVocab = [];
      let re = RegExp("^" + input, "g");
      for (let i = 0; i < this.allVocab.length; i++) {
        let match = this.allVocab[i].search(re);
        if (match != -1) {
          this.showedVocab.push(this.allVocab[i]);
        }
      }
    },
  },
  methods: {
    //TODO: search dynamically by each letter user type in
    // have a list of vocab and use regular expression to look for the target
    searchWord: function () {
      if (this.userInput == null || this.userInput == "") {
        alert("Please enter a word before searching.");
      } else {
        console.log(this.userInput);
        this.addToHistory(this.userInput);
        console.log(this.history);
      }
    },
    addToHistory: function (word) {
      this.history.push({ word: word, id: null });
      if (this.history.length > 5) {
        this.history.shift();
      }
      for (let i in this.history) {
        this.history[i].id = i;
      }
    },
    showVocab: function (vocab, isHistory = false) {
      this.is_search_visible = false;
      this.is_history_visible = false;
      this.is_vocab_page_visible = true;
      this.API.getVocabByText(vocab)
        .then((resp) => resp.json())
        .then((json) => {
          if (json.status == "ok") {
            this.selectedVocab = json;
            !isHistory ? this.addToHistory(vocab) : {};
          } else {
            //TODO: alert for now, planning to add an error message displayer
            alert(json.message);
          }
          console.log(this.selectedVocab);
        });
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
    },
  },
};
</script>

<style scoped>
.dictionary input {
  text-align: center;
  width: 25%;
  padding: 5px 0px 5px 0px;
}

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

.result {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  height: 50vh;
  overflow-y: scroll;
  width: 100%;
  border-radius: 10px;
  padding: 5px 5px 5px 5px;
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