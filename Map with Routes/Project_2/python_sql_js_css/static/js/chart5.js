
		Chart.defaults.global.pointHitDetectionRadius = 1;

		var customTooltips = function(tooltip) {
			// Tooltip Element
			var tooltipEl = document.getElementById('chartjs-tooltip');

			if (!tooltipEl) {
				tooltipEl = document.createElement('div');
				tooltipEl.id = 'chartjs-tooltip';
				tooltipEl.innerHTML = '<table></table>';
				this._chart.canvas.parentNode.appendChild(tooltipEl);
			}

			// Hide if no tooltip
			if (tooltip.opacity === 0) {
				tooltipEl.style.opacity = 0;
				return;
			}

			// Set caret Position
			tooltipEl.classList.remove('above', 'below', 'no-transform');
			if (tooltip.yAlign) {
				tooltipEl.classList.add(tooltip.yAlign);
			} else {
				tooltipEl.classList.add('no-transform');
			}

			function getBody(bodyItem) {
				return bodyItem.lines;
			}

			// Set Text
			if (tooltip.body) {
				var titleLines = tooltip.title || [];
				var bodyLines = tooltip.body.map(getBody);

				var innerHtml = '<thead>';

				titleLines.forEach(function(title) {
					innerHtml += '<tr><th>' + title + '</th></tr>';
				});
				innerHtml += '</thead><tbody>';

				bodyLines.forEach(function(body, i) {
					var colors = tooltip.labelColors[i];
					var style = 'background:' + colors.backgroundColor;
					style += '; border-color:' + colors.borderColor;
					style += '; border-width: 2px';
					var span = '<span class="chartjs-tooltip-key" style="' + style + '"></span>';
					innerHtml += '<tr><td>' + span + body + '</td></tr>';
				});
				innerHtml += '</tbody>';

				var tableRoot = tooltipEl.querySelector('table');
				tableRoot.innerHTML = innerHtml;
			}

			var positionY = this._chart.canvas.offsetTop;
			var positionX = this._chart.canvas.offsetLeft;

			// Display, position, and set styles for font
			tooltipEl.style.opacity = 1;
			tooltipEl.style.left = positionX + tooltip.caretX + 'px';
			tooltipEl.style.top = positionY + tooltip.caretY + 'px';
			tooltipEl.style.fontFamily = tooltip._bodyFontFamily;
			tooltipEl.style.fontSize = tooltip.bodyFontSize + 'px';
			tooltipEl.style.fontStyle = tooltip._bodyFontStyle;
			tooltipEl.style.padding = tooltip.yPadding + 'px ' + tooltip.xPadding + 'px';
		};
        
     var currentKey = "very_close";
     var currentType = "UberPool";
     //lineChartData = {};  
    
        
    var lindata = function generateData(key,type) {
        $.getJSON("/chartsinfo", function(data) { 
               console.log(key);
               console.log(type);
            cplaces = [];
            places = [];
            for (var i = 0; i< data[0].length; i++){
               places.push(data[0][i][0]);}
            times = [];
            for (var j = 0; j< data[1].length; j++){
               times.push(data[1][j][0]);}
             types = [];
            for (var k = 0; k< data[2].length; k++){
               types.push(data[2][k][0]);}
            console.log(places);
            console.log(times);
            console.log(types);
            if (currentKey == "very_close") {
            cplaces = [places[0],places[1],places[2],places[3],places[4]];
            }
             if (currentKey == "close") {
            cplaces = [places[5],places[6],places[7],places[8],places[9]];
             }
             if (currentKey == "far") {
            cplaces = [places[10],places[11],places[12],places[13],places[14]];
             }
            if (currentKey == "very_far") {
            cplaces = [places[15],places[16],places[17],places[18],places[19]];
            }
            console.log(cplaces);
            console.log(data[3][3][0]);
            console.log(data[3][3][6]);
            // data[0][m][0] ---- name of place
            sub0 =[];
            sub1 = [];
            sub2 = [];
            sub3 = [];
            sub4 = [];
                for (var n = 0; n < data[3].length ; n++) {
                    if ((data[3][n][0] == cplaces[0]) & (data[3][n][6] == type)) {
                        sub0.push(data[3][n][2])
                    }
                    if ((data[3][n][0] == cplaces[1]) & (data[3][n][6] == type)) {
                        sub1.push(data[3][n][2])
                    }
                    if ((data[3][n][0] == cplaces[2]) & (data[3][n][6] == type)) {
                        sub2.push(data[3][n][2])
                    }
                    if ((data[3][n][0] == cplaces[3]) & (data[3][n][6] == type)) {
                        sub3.push(data[3][n][2])
                    }
                    if ((data[3][n][0] == cplaces[4]) & (data[3][n][6] == type)) {
                        sub4.push(data[3][n][2])
                    }
                }
              console.log(sub0);
              console.log(sub3);
        
		var lineChartData = {
			labels: times,
			datasets: [{
				label: cplaces[0],
				borderColor: window.chartColors.red,
				pointBackgroundColor: window.chartColors.red,
				fill: false,
				data: sub0
			}, {
				label: cplaces[1],
				borderColor: window.chartColors.blue,
				pointBackgroundColor: window.chartColors.blue,
				fill: false,
				data: sub1
			}, {
				label: cplaces[2],
				borderColor: window.chartColors.orange,
				pointBackgroundColor: window.chartColors.orange,
				fill: false,
				data: sub2
			}, {
				label: cplaces[3],
				borderColor: window.chartColors.green,
				pointBackgroundColor: window.chartColors.green,
				fill: false,
				data: sub3
			}, {
				label: cplaces[4],
				borderColor: window.chartColors.purple,
				pointBackgroundColor: window.chartColors.purple,
				fill: false,
				data: sub4
			}
                
                ]
		};
            console.log(lineChartData)
           // return lineChartData
        });
        //return lineChartData;
        chartEl.data = lineChartData;
    };

		

		/*document.getElementById('select-key').addEventListener('change', function() {
			var e = document.getElementById('select-key');
            var value = e.options[e.selectedIndex].value;
            currentKey = value;
            //generateData(currentKey, currentType);
			//window.myLine.update();
            var chartEl = document.getElementById('chart');
			window.myLine = new Chart(chartEl, {
				type: 'line',
				data: generateData(currentKey, currentType),
				options: {
					title: {
						display: true,
						text: 'Chart.js Line Chart - Custom Tooltips'
					},
					tooltips: {
						enabled: false,
						mode: 'index',
						position: 'nearest',
						custom: customTooltips
					}
				}
			});
           
		});    */                     
                                 
        window.onload = function () {
            //lineChartData = {};
            console.log(currentKey);
            console.log(currentType);
            //generateData(currentKey, currentType);
            //console.log(lineChartData);
            var chartEl = document.getElementById('chart');
			window.myLine = new Chart(chartEl, {
				type: 'line',
				data: lindata,
				options: {
					title: {
						display: true,
						text: 'Chart.js Line Chart - Custom Tooltips'
					},
					tooltips: {
						enabled: false,
						mode: 'index',
						position: 'nearest',
						custom: customTooltips
					}
				}
			});
            //window.myline.update()
            
        }                         

        
	