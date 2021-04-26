<template>
  <div class="testQuestion">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="error" class="error">
      {{ error }}
    </div>
    <div v-if="is_testOptions_visible" class="testText">
      <a class="goBackButton" v-on:click="returnButtonAction">
        &larr; Go Back</a
      >
      <span>{{ currentVocabId + "/" + Object.keys(vocabMap).length }}</span>
      <label id="testQuestionText" for="ans">
        <h2>{{ vocabMap[currentVocabId].text }}</h2>
      </label>
      <div class="testOptions">
        <div>
          <input
            type="radio"
            name="ans"
            v-bind:value="0"
            v-model="ans_picked"
          />
          <label for="0"
            >{{ optionsMap[currentVocabId].option[0].split("*")[0] }}
          </label>
          <br />
          <input
            type="radio"
            name="ans"
            v-bind:value="1"
            v-model="ans_picked"
          />
          <label for="1"
            >{{ optionsMap[currentVocabId].option[1].split("*")[0] }}
          </label>
          <br />
          <input
            type="radio"
            name="ans"
            v-bind:value="2"
            v-model="ans_picked"
          />
          <label for="2"
            >{{ optionsMap[currentVocabId].option[2].split("*")[0] }}
          </label>
          <br />
          <input
            type="radio"
            name="ans"
            v-bind:value="3"
            v-model="ans_picked"
          />
          <label for="3"
            >{{ optionsMap[currentVocabId].option[3].split("*")[0] }}
          </label>
        </div>
      </div>

      <div class="testAns" v-if="show_ans">
        <p class="questionResult" v-bind:style="questionResultStyle">
          {{ question_result }}
        </p>
        <h4>
          {{ question_ans }}
        </h4>
      </div>
      <div class="testButtons">
        <span
          id="submit"
          v-on:click="submitButtonAction"
          v-if="is_submitButton_visible"
        >
          {{ submit_button_text }}
        </span>
        <span id="result" v-on:click="showTestResult()">View Result</span>
      </div>
    </div>
    <div class="testResult" v-if="show_test_result">
      <a class="goBackButton" v-on:click="returnButtonAction">&larr; Go Back</a>
      <p class="resultSummary">{{ showTestResult() }}</p>
      <span
        v-for="vocab in wrongList"
        v-bind:key="vocab.id"
        v-on:click="showVocabPage(vocab)"
      >
        {{ vocab.text }}
      </span>
    </div>
    <div v-if="is_vocab_page_visible">
      <VocabPage
        v-bind:vocabData="vocabData"
        v-on:goBack="goBackButtonAction"
      ></VocabPage>
    </div>
  </div>
</template>

<script>
import VocabPage from "./VocabPage";

//TODO: this is a code copied from : https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
function shuffle(array) {
  var currentIndex = array.length,
    temporaryValue,
    randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

function vocabToString(vocab) {
  let str = "";
  str =
    vocab.text +
    "\t" +
    vocab.definition +
    "\t[ " +
    vocab.vocabRoot +
    " ]\timportancy: " +
    vocab.importancy;
  return str;
}

export default {
  name: "TestQuestion",
  components: {
    VocabPage,
  },
  props: {
    unit: Number,
    api_fetched_data: Promise,
  },
  data() {
    return {
      loading: false,
      // test properties
      text: null,
      def: null,
      error: null,
      vocabMap: null,
      optionsMap: null,
      currentVocabId: 1,
      isTestEnded: false,
      //submit button control
      submit_button_text: "Submit",
      ans_picked: null,
      question_result: "",
      wrongList: [],
      question_ans: "",
      isQuestionAnswered: false,
      // visible controler
      show_ans: false,
      show_test_result: false,
      is_testOptions_visible: false,
      is_submitButton_visible: true,
      is_vocab_page_visible: false,
      //vocabPage Data properties
      vocabData: {},
      //dynamic style object
      questionResultStyle: { color: "" },
    };
  },
  created() {
    // fetch the data when the view is created and the data is
    // already being observed
    this.loading = true;
    this.is_testOptions_visible = false;
    this.api_fetched_data
      .then((resp) => resp.json())
      .then((json) => {
        this.createQuestions(json);
        this.loading = false;
        this.is_testOptions_visible = true;
      });
  },
  //   watch: {
  //     // call again the method if the route changes
  //     $route: "fetchData",
  //   },
  methods: {
    createQuestions(jsonData) {
      this.error = this.text = this.def = null;
      this.text = jsonData[0].vocab.text;
      this.def = jsonData[0].vocab.definition;
      this.vocab = jsonData[0].vocab.text;

      let vocabMap = {};
      let optionsMap = {};
      let id = 1;
      for (let tq in jsonData) {
        jsonData[tq].vocab["id"] = id;
        vocabMap[id] = jsonData[tq].vocab;
        let option_obj = {};
        option_obj["id"] = id;
        jsonData[tq].options.push(jsonData[tq].vocab.definition + "*");
        option_obj["option"] = shuffle(jsonData[tq].options);
        optionsMap[id] = option_obj;
        id++;
      }
      this.vocabMap = vocabMap;
      this.optionsMap = optionsMap;
    },
    submitButtonAction() {
      if (this.submit_button_text == "Submit") {
        let curOpt = this.optionsMap[this.currentVocabId].option;
        let curVocab = this.vocabMap[this.currentVocabId];
        if (this.ans_picked == null) {
          alert("Please select an option before clicking 'Submit' ");
        } else {
          let selectedAns = curOpt[this.ans_picked];
          //handle ans correctness
          if (selectedAns.charAt(selectedAns.length - 1) == "*") {
            this.question_result = "Correct";
            this.questionResultStyle.color = "green";
          } else {
            this.addToWrongList(curVocab);
            this.question_result = "Wrong";
            this.questionResultStyle.color = "red";
          }
          this.question_ans = vocabToString(curVocab);
          this.show_ans = true;
          this.isQuestionAnswered = true;
          if (this.currentVocabId + 1 > Object.keys(this.vocabMap).length) {
            this.is_submitButton_visible = false;
            this.testEndAction();
          } else {
            this.submit_button_text = "Next Question";
          }
        }
      } else if (this.submit_button_text == "Next Question") {
        this.currentVocabId += 1;
        this.show_ans = false;
        this.ans_picked = null;
        this.isQuestionAnswered = false;
        this.submit_button_text = "Submit";
      }
    },
    showTestResult() {
      this.show_test_result = true;
      this.is_testOptions_visible = false;
      let ansCount = this.isQuestionAnswered
        ? this.currentVocabId
        : this.currentVocabId - 1;
      let correctCount = ansCount - this.wrongList.length;
      let total = Object.keys(this.vocabMap).length;
      let resultData =
        "You have answered " +
        ansCount.toString() +
        " questions , with " +
        +correctCount.toString() +
        " correct." +
        " This test has a total of " +
        total.toString() +
        " questions";
      return resultData;
    },
    addToWrongList(vocab) {
      this.wrongList.push(vocab);
      console.log(vocab);
    },
    vocabToString(vocab) {
      let str = "";
      str =
        vocab.text +
        "\t" +
        vocab.definition +
        "\t[ " +
        vocab.vocabRoot +
        " ]\timportancy: " +
        vocab.importancy;
      return str;
    },
    returnButtonAction: function () {
      if (this.show_test_result && this.isTestEnded == false) {
        this.show_test_result = false;
        this.is_testOptions_visible = true;
      } else {
        this.$emit("return");
      }
    },
    testEndAction: function () {
      this.is_testOptions_visible = false;
      this.isTestEnded = true;
      this.showTestResult();
    },
    // click the vocab from the wrong list
    showVocabPage: function (vocab) {
      this.vocabData = vocab;
      this.is_vocab_page_visible = true;
      this.show_test_result = false;
    },
    goBackButtonAction: function () {
      this.is_vocab_page_visible = false;
      this.show_test_result = true;
    },
  },
};
</script>

<style scoped>
.testQuestion {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.loading {
  font-size: 30px;
}

.testText {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.testOptions {
  margin: 0 25% 0 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: left;
}

.questionResult {
  color: green;
}

.testButtons {
  display: flex;
  flex-direction: row-reverse;
  justify-content: space-evenly;
  margin: 2vh 0 0 0;
}

.goBackButton {
  align-self: flex-start;
}

.goBackButton,
#submit,
#result {
  width: 50;
  padding: 8px 10px 8px 10px;
  border-style: none;
  background-color: #c1c4ca;
  border-radius: 10px;
  color: black;
}

.goBackButton:hover,
#submit:hover,
#result:hover {
  background-color: #acaeb4;
}

.goBackButton:active,
#submit:active,
#result :active {
  background-color: #96989d;
}

.testResult {
  display: flex;
  flex-direction: column;
}

.resultSummary {
  font-size: 24px;
}

.testResult span:not(.resultSummary) {
  padding: 1px 0 1px 0;
  border-style: none;
  border-radius: 10px;
  background-color: #c1c4ca;
  margin: 5px 0 0 0;
}

.testResult span:not(.resultSummary):hover {
  background-color: #acaeb4;
}

.testResult span:not(.resultSummary):active {
  background-color: #96989d;
}
</style>
