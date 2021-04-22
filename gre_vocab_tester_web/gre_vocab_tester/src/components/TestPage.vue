<template>
  <div class="TestPage">
    <div class="unitSelection" v-if="is_unit_selection_visible">
      <h3>Please select which unit you want to be tested</h3>
      <span
        v-for="unit in allUnits"
        v-bind:key="unit.unitName"
        v-on:click="unitButtonAction(unit.unitNum)"
      >
        {{ unit.unitName }}
      </span>
      <!-- TODO: remove this when done testing -->
      <span v-on:click="testMethod()">TESTING</span>
    </div>
    <div class="testQuestionPage" v-if="is_tq_visible">
      <TestQuestion
        v-bind:api_fetched_data="unitTestDataPromise"
        v-on:return="showUnitSelection()"
      ></TestQuestion>
    </div>
  </div>
</template>

<script>
import TestQuestion from "./TestQuestion";

export default {
  name: "TestPage",
  components: { TestQuestion },
  props: { api_fetched_data: Promise, API: Object },
  created() {
    this.api_fetched_data
      .then((resp) => resp.json())
      .then((json) => {
        console.log(json);
        this.allUnits = json;
        return json;
      });
  },
  data() {
    return {
      selectedUnit: null,
      allUnits: [],
      unitTestDataPromise: null,
      is_unit_selection_visible: true,
      is_tq_visible: false,
    };
  },
  methods: {
    // createUnitList: function (unitList) {},
    unitButtonAction: function (unitNum) {
      this.selectedUnit = unitNum;
      let unitTestData = this.API.getTestByUnit(unitNum);
      this.unitTestDataPromise = unitTestData;
      this.hideUnitSelection();
      //   unitTestData
      //     .then((resp) => resp.json())
      //     .then((json) => {
      //       console.log(json);
      //     });
    },
    hideUnitSelection: function () {
      this.is_unit_selection_visible = false;
      this.is_tq_visible = true;
    },
    showUnitSelection: function () {
      this.is_unit_selection_visible = true;
      this.is_tq_visible = false;
    },
    testMethod: function () {
      this.selectedUnit = "TESTING";
      let unitTestData = this.API.testMethod();
      this.unitTestDataPromise = unitTestData;
      this.hideUnitSelection();
    },
  },
};
</script>

<style scoped>
.unitSelection {
  display: flex;
  flex-direction: column;
}

.unitSelection span {
  width: 50;
  padding: 10px 10px 10px 10px;
  margin: 0px 25% 10px 25%;
  margin-bottom: 10px;
  border-style: none;
  border: 1px 1px 1px 1px;
  background-color: #c1c4ca;
  border-radius: 10px;
  color: black;
}

.unitSelection span:hover {
  background-color: #acaeb4;
}

.unitSelection span:active {
  background-color: #96989d;
}
</style>