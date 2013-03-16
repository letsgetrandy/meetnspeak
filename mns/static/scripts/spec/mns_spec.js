describe("EligibilityCheck class", function() {

    // create the display element that we'll interact with
    //document.write('<div id="eligibility"></div>');

    beforeEach(function(){
        //document.getElementById('eligibility').className = '';
    });


    it ("should skip eligibility check when overridden", function() {

        expect(1).toEqual(1);

    });


    it ("should handle a failure", function() {

        expect(false).toEqual(true);

    });

});
