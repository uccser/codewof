/**
 * Make a request to calculate and obtain the HTML of a user's recommended questions, and place them on the page.
 */
$.ajax({
    type: 'GET',
    url: getRecommendedQuestionsURL(),
    async: true,
    cache: true,
    headers: {"X-CSRFToken": csrftoken},
    success: function (data, textStatus, xhr) {
        const recommendedQuestions = data['recommended_questions'];
        if (recommendedQuestions.length === 2) {
            document.getElementById('question-1').innerHTML = recommendedQuestions[0]
            document.getElementById('question-2').innerHTML = recommendedQuestions[1]
        } else {
            document.getElementById('recommendations').innerHTML =
                '<div class="alert alert-secondary" role="alert">\n' +
                '<strong>Sorry!</strong> We currently don\'t have any question recommendations for you.\n' +
                '</div>'
        }
    },
});
