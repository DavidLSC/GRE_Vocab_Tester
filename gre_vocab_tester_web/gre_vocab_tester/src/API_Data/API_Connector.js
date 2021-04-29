class API_Connector {
    constructor(api_url) {
        this.api_url = api_url;
    }


    API_fetch(url, method = "GET", data = null) {
        let resp = fetch(url, {
            method: method,
            body: JSON.stringify(data)
        });
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

    //addErrorCount request data
    //{
    //  "text": vocab_text,
    //  "errorCount" : error_number_needed_to_be_added
    //}
    addErrorCount(jsonData) {
        return this.API_fetch(this.api_url + "/addErrorCount/", method = "POST", data = jsonData);
    }

    //addSampleSentence request data
    //{
    //  "text": vocab_text,
    //  "sentence" : sample sentence
    //}
    addSampleSentence(jsonData) {
        return this.API_fetch(this.api_url + "/addSampleSentence/", method = "POST", data = jsonData);
    }

    //TODO: create a really short test so we can test what happens when the test ended
    testMethod() {
        return this.API_fetch(this.api_url + "/test");
    }

}

export default API_Connector;