/*
 *  Kuma Gauge - v0.2
 *
 *  Made by Sam Bellen for Kunstmaan
 *   - http:// www.kunstmaan.be
 *   - http:// www.sambellen.be
 *
 *  Under MIT License
 */

;(function ( $, window, document, undefined ) {
    var config = {
        radius : 80,
        paddingX : 40,
        paddingY : 40,
        gaugeWidth : 30,

        fill : '0-#1cb42f:0-#fdbe37:50-#fa4133:100',
        gaugeBackground : '#f4f4f4',
        background : '#fff',

        showNeedle : true,

        animationSpeed : 500,

        width : 0,
        height : 0,
        centerX : 0,
        centerY : 0,

        min : 0,
        max : 100,
        value : 80,

        valueLabel : {
            display : true,
            fontFamily : 'Arial',
            fontColor : '#000',
            fontSize : '20',
            fontWeight : 'normal'
        },
        title : {
            display : true,
            value : '',
            fontFamily : 'Arial',
            fontColor : '#000',
            fontSize : '20',
            fontWeight : 'normal'
        },
        label : {
            display : true,
            left : 'Low',
            right : 'High',
            fontFamily : 'Arial',
            fontColor : '#000',
            fontSize : '12',
            fontWeight : 'normal'
        }
    };

    // Create an arc with raphael.js
    Raphael.fn.arc = function(startX, startY, endX, endY, radius1, radius2, angle) {
        var arcSVG = [radius1, radius2, angle, 0, 1, endX, endY].join(' ');
        return this.path('M' + startX + ' ' + startY + ' a ' + arcSVG);
    };

    // Calculate a circular arc with raphael.js
    Raphael.fn.circularArc = function(centerX, centerY, radius, startAngle, endAngle) {
        var startX = centerX + radius * Math.cos(startAngle * Math.PI / 180);
        var startY = centerY + radius * Math.sin(startAngle * Math.PI / 180);
        var endX = centerX + radius * Math.cos(endAngle * Math.PI / 180);
        var endY = centerY + radius * Math.sin(endAngle * Math.PI / 180);
        return this.arc(startX, startY, endX-startX, endY-startY, radius, radius, 0);
    };

    // The kuma Gauge constructor
    function kumaGauge(element, options , method) {
        // This
        var _this = this;

        // The element
        _this.element = element;
        _this.$element = $(element);

        // The config
        _this.config = $.extend( {}, config, options );
        _this._config = config;

        _this.method = method;

        // The actual gauge
        _this.gauge = {};

        // Initialise
        _this.init();
    }

    // Extend the kumaGauge object
    kumaGauge.prototype = {
        init: function () {
            // this
            _this = this;

            if (!_this.method) {
                _this.draw();
            }
        },
        _setup : function() {
            // This
            _this = this;

            // Calculate some values needed do draw the gauge
            _this.config.width = (_this.config.radius * 2) + (_this.config.paddingX * 2);
            _this.config.height = _this.config.radius + (_this.config.paddingY * 2);
            _this.config.centerX = _this.config.paddingX + _this.config.radius;
            _this.config.centerY = _this.config.paddingY + _this.config.radius;

            // The div wich acts as the canvas needs an id, so we give it a unique one if it doesn't have one
            if (typeof $(this).attr('id') === 'undefined' || $(this).attr('id') === '') {
                _this.config.id = 'gauge-' + $('*[id^="gauge-"]').length;
                _this.$element.attr('id', _this.config.id);
            }
        },
        _calculateRotation : function(min, max, val) {
            var _range, _rotation;
            _range = max - min;

            if (val < max && val > min) {
                _rotation = 180 * ((val - min) / _range);
            } else if (val <= min){
                _rotation = 0;
            } else {
                _rotation = 180;
            }

            return _rotation;
        },
        draw : function() {
            //this
            var _this = this;

            // Setup all the needed config variables
            _this._setup();

            // Make the base drawing Canvas
            _this.gauge = new Raphael(_this.config.id, _this.config.width, _this.config.height);

            // Draw the gauge
            _this.gauge.gauge = _this.gauge.circularArc(_this.config.centerX, _this.config.centerY,
                           _this.config.radius, 180, 0);
            _this.gauge.gauge.attr({
                'fill' : _this.config.fill,
                'stroke' : 'none'
            });
            _this.gauge.gauge.node.setAttribute('class', 'gauge');

            // Draw the gauge background
            _this.gauge.gaugeBackground = _this.gauge.circularArc(_this.config.centerX, _this.config.centerY,
                                     _this.config.radius, 180, 0);
            _this.gauge.gaugeBackground.attr({
                'fill' : _this.config.gaugeBackground,
                'stroke' : 'none'
            });
            _this.gauge.gaugeBackground.node.setAttribute('class', 'gauge__background');

            // Draw the white center arc
            _this.gauge.centerArc = _this.gauge.circularArc(_this.config.centerX, _this.config.centerY,
                               _this.config.radius - _this.config.gaugeWidth, 180, 0);
            _this.gauge.centerArc.attr({
                'fill' : _this.config.background,
                'stroke' : 'none'
            });
            _this.gauge.centerArc.node.setAttribute('class', 'gauge__center');

            // Draw the needle
            if (_this.config.showNeedle) {
                _this.gauge.needle = _this.gauge.rect(_this.config.centerX, _this.config.paddingY, 1, 40);
                _this.gauge.needle.attr({
                    'fill' : '#000',
                    'stroke' : 'none'
                });
                _this.gauge.needle.node.setAttribute('class', 'gauge__needle');
            }

            // Draw the bottom mask to hide the rotated background arc
            _this.gauge.bottomMask = _this.gauge.rect(0, _this.config.centerY, _this.config.width, 40);
            _this.gauge.bottomMask.attr({
                'fill' : _this.config.background,
                'stroke' : 'none'
            });

            // Draw the text container for the value
            if (_this.config.valueLabel.display) {
                if (_this.config.showNeedle) {
                    _this.gauge.valueLabel = _this.gauge.text(_this.config.centerX, _this.config.centerY - 10,
                                        Math.round((_this.config.max - _this.config.min) / 2));
                } else {
                    _this.gauge.valueLabel = _this.gauge.text(_this.config.centerX, _this.config.centerY - 10,
                                        _this.config.value);
                }
                _this.gauge.valueLabel.attr({
                    'fill' : _this.config.valueLabel.fontColor,
                    'font-size' : _this.config.valueLabel.fontSize,
                    'font-family' : _this.config.valueLabel.fontColor,
                    'font-weight' : _this.config.valueLabel.fontWeight
                });
                _this.gauge.valueLabel.node.setAttribute('class', 'gauge__value');
            }

            // Draw the title
            if (_this.config.title.display) {
                _this.gauge.title = _this.gauge.text(_this.config.centerX, _this.config.paddingY - 5,
                                   _this.config.title.value);
                _this.gauge.title.attr({
                    'fill' : _this.config.title.fontColor,
                    'fill-opacity' : 0,
                    'font-size' : _this.config.title.fontSize,
                    'font-family' : _this.config.title.fontFamily,
                    'font-weight' : _this.config.title.fontWeight
                });
                _this.gauge.title.node.setAttribute('class', 'gauge__title');
            }

            if (_this.config.label.display) {
                // Draw the left label
                _this.gauge.leftLabel = _this.gauge.text((_this.config.gaugeWidth / 2) + _this.config.paddingX,
                                   _this.config.centerY + 10, _this.config.label.left);
                _this.gauge.leftLabel.attr({
                    'fill' : _this.config.title.fontColor,
                    'fill-opacity' : 0,
                    'font-size' : _this.config.label.fontSize,
                    'font-family' : _this.config.label.fontFamily,
                    'font-weight' : _this.config.label.fontWeight
                });
                _this.gauge.leftLabel.node.setAttribute('class', 'gauge__label--left');

                // Draw the right label
                _this.gauge.rightLabel = _this.gauge.text((_this.config.width - (_this.config.gaugeWidth / 2)) - _this.config.paddingX,
                                    _this.config.centerY + 10, _this.config.label.right);
                _this.gauge.rightLabel.attr({
                    'fill' : _this.config.title.fontColor,
                    'fill-opacity' : 0,
                    'font-size' : _this.config.label.fontSize,
                    'font-family' : _this.config.label.fontFamily,
                    'font-weight' : _this.config.label.fontWeight
                });
                _this.gauge.rightLabel.node.setAttribute('class', 'gauge__label--right');
            }

            // There is a bug with raphael.js and webkit which renders text element at double the Y value.
            // Resetting the Y values after a timeout fixes this.
            // See https://github.com/DmitryBaranovskiy/raphael/issues/491
            setTimeout(function() {
                if (_this.config.valueLabel.display) {
                    _this.gauge.valueLabel.attr('y', _this.config.centerY - 10);
                }

                if (_this.config.title.display) {
                    _this.gauge.title.attr({
                        'y' : _this.config.paddingY - (_this.gauge.title.getBBox().height / 2),
                        'fill-opacity' : 1
                    });
                }

                if (_this.config.label.display) {
                    _this.gauge.leftLabel.attr({
                        'y' : _this.config.centerY + (_this.gauge.leftLabel.getBBox().height / 2),
                        'fill-opacity' : 1,
                    });
                    _this.gauge.rightLabel.attr({
                        'y' : _this.config.centerY + (_this.gauge.rightLabel.getBBox().height / 2),
                        'fill-opacity' : 1,
                    });
                }
            }, 1000);

            // Animate the gauge to the right value position
            _this.gauge.gaugeBackground.animate({transform:'r' +
                            _this._calculateRotation(_this.config.min, _this.config.max, _this.config.value) + ',' +
                            _this.config.centerX + ',' + _this.config.centerY}, _this.config.animationSpeed, '<>');

        },
        update: function (data) {
            //this
            var _this = this;

            var  updateGauge = function(min, max, value) {
                _this.config.min = min;
                _this.config.max = max;
                _this.config.value = value;

                // Update the rotation of the gauge
                _this.gauge.gaugeBackground.animate({transform:'r' +
                    _this._calculateRotation(min, max, value) + ',' +
                    _this.config.centerX + ',' + _this.config.centerY}, _this.config.animationSpeed, '<>');

                // Update the value label
                if (_this.config.valueLabel.display) {
                    if (_this.config.showNeedle) {
                        _this.gauge.valueLabel.attr('text', value);
                    } else {
                        _this.gauge.valueLabel.attr('text', (max - min) / 2);
                    }
                }
            };

            if (typeof data.min !== 'undefined' && typeof data.max !== 'undefined' && typeof data.value !== 'undefined') {
                updateGauge(data.min, data.max, data.value);
            } else if (typeof data.value !== 'undefined') {
                updateGauge(_this.config.min, _this.config.max, data.value);
            }
        }
    };

    $.fn.kumaGauge = function ( method, options ) {
        var _method = method,
            _arguments = arguments,
            _this = this;

        if (typeof _method !== 'string') {
            if (_arguments.length === 1 ) {
                options = _method;
                method = false;

                return this.each(function() {
                    if ( !$.data( this, 'kumaGauge' ) ) {
                        $.data( this, 'kumaGauge', new kumaGauge( this, options, method ) );
                    }
                });
            }
        } else {
            return this.each(function() {
                if (typeof $.data(this, 'kumaGauge')[method] === 'function') {
                    $.data(this, 'kumaGauge')[method](options);
                }
            });
        }


    };

})( jQuery, window, document );
