class API_Connector {
    constructor(api_url) {
        this.api_url = api_url;
    }


    API_fetch(url) {
        let resp = fetch(url);
        return resp;
    }

    getAllTest() {
        return this.API_fetch(this.api_url + "/getAllTest");
    }

    getTestByUnit(unitNum) {
        return this.API_fetch(this.api_url + "/getTestByUnit/" + unitNum.toString());
    }

    getAllUnits() {
        return this.API_fetch(this.api_url + "/getAllUnits");
    }

    getAllVocabText() {
        return this.API_fetch(this.api_url + "/getAllVocabText");
    }

    getVocabByText(vocabText) {
        return this.API_fetch(this.api_url + "/getVocabByText/" + vocabText);
    }

    //TODO: create a really short test so we can test what happens when the test ended
    testMethod() {
        return this.API_fetch(this.api_url + "/test");
    }

}

export default API_Connector;