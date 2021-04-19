<template>
  <div class="testQuestion">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="error" class="error">
      {{ error }}
    </div>
    <span id="testQuestionReturn" v-on:click="returnButtonAction">
      &larr; Return</span
    >
    <div v-if="text" class="testText">
      <span>{{ currentVocabId }}</span>
      <span>/</span>
      <span>{{ Object.keys(vocabMap).length }}</span>
      <div class="test-options">
        <label id="test-question-text" for="ans">
          <h2>{{ vocabMap[currentVocabId].text }}</h2>
        </label>
        <p>
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
        </p>
      </div>

      <div class="testAns" v-if="show_ans">
        <p class="question-result">{{ question_result }}</p>
        <h4>
          {{ question_ans }}
        </h4>
      </div>
      <div class="testButtons">
        <span id="submit" v-on:click="submitButtonAction">
          {{ submit_button_text }}
        </span>
        <span id="result" v-on:click="resultButtonAction">See Result</span>
      </div>

      <div class="TestResult" v-if="show_test_result">
        <ul>
          <li v-for="vocab in wrongList" v-bind:key="vocab.id">
            {{ vocabToString(vocab) }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
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
      //submit button control
      submit_button_text: "Submit",
      ans_picked: null,
      question_result: "",
      wrongList: [],
      question_ans: "",
      // visible controler
      show_ans: false,
      show_test_result: false,
    };
  },
  created() {
    // fetch the data when the view is created and the data is
    // already being observed
    this.loading = true;
    this.api_fetched_data
      .then((resp) => resp.json())
      .then((json) => {
        this.createQuestions(json);
      });
  },
  //   watch: {
  //     // call again the method if the route changes
  //     $route: "fetchData",
  //   },
  methods: {
    createQuestions(jsonData) {
      this.error = this.text = this.def = null;
      this.loading = false;
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
        }
        let selectedAns = curOpt[this.ans_picked];
        //handle ans correctness
        if (selectedAns.charAt(selectedAns.length - 1) == "*") {
          this.question_result = "Correct";
        } else {
          this.addToWrongList(curVocab);
          this.question_result = "Wrong";
        }
        this.question_ans = vocabToString(curVocab);
        this.show_ans = true;
        this.submit_button_text = "Next Question";
      } else if (this.submit_button_text == "Next Question") {
        this.currentVocabId += 1;
        this.show_ans = false;
        this.ans_picked = null;
        this.submit_button_text = "Submit";
      }
    },
    resultButtonAction() {
      this.show_test_result = true;
      let ansCount = this.currentVocabId;
      let correctCount = ansCount - this.wrongList.length;
      let total = Object.keys(this.vocabMap).length;
      console.log(correctCount, "/", ansCount, " out of ", total);
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
      this.$emit("return");
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

.testButtons {
  display: flex;
  flex-direction: row-reverse;
  justify-content: space-evenly;
}

#testQuestionReturn {
  width: 100px;
}

#testQuestionReturn,
#submit,
#result {
  width: 50;
  padding: 10px 10px 10px 10px;
  border-style: none;
  background-color: #c1c4ca;
  border-radius: 10px;
  color: black;
}

#testQuestionReturn:hover,
#submit:hover,
#result:hover {
  background-color: #acaeb4;
}

#testQuestionReturn:active,
#submit:active,
#result :active {
  background-color: #96989d;
}
</style>
