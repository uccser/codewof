
var calculate_fitness_score = function(n_target) {
    var fitness_score = 100;
    var recency_weights = [0.5, 2, 1.5, 0.75, 0.25];

    for (var i = 0; i < 5; i++) {
        var n_attempts = $("#week" + i).text();
    
        if (+n_attempts < +n_target) {
            
            var percent_away_from_goal = 1 - (+n_attempts / +n_target);
            var penalty = 20 * recency_weights[i] * percent_away_from_goal;
    
            fitness_score -= penalty;
        }
    }
    return parseInt(fitness_score);
}

var default_choice = $('#goal_choice').val();
var fitness_score = calculate_fitness_score(default_choice);

$('.gauge').kumaGauge({
    value : fitness_score,
    radius: 90,
    gaugeWidth: 40,
    fill : '0-#fa4133:0-#ffaa00:35-#fdee37:50-#1cb42f:100',
    showNeedle: false,
    label: {
        display: false,
    }
});



$('#goal_choice').change(function() {
    var choice = $('#goal_choice').val();

    $.ajax({
        url: '/ajax/save_goal_choice/',
        type: 'POST',
        method: 'POST',
        data: {
            goal_choice: choice,
            csrfmiddlewaretoken: window.CSRF_TOKEN
        },
        dataType: 'json',
        success: function(result) {
            var score = calculate_fitness_score(choice);
            console.log(score);
            $('.gauge').kumaGauge('update', {
                value: score
            });
        }
    });
});