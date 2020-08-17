// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var config = {
  type: 'line',
  data: {
    datasets: [{
      label: "Value",
      lineTension: 0.3,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgba(78, 115, 223, 1)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(78, 115, 223, 1)",
      pointBorderColor: "rgba(78, 115, 223, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
      pointHoverBorderColor: "rgba(78, 115, 223, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: [],
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },

    scales: {
      xAxes: [{
        type: 'time',
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Timestamp'
        },
        ticks: {
          major: {
            fontStyle: 'bold',
            fontColor: '#FF0000'
          }
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'value'
        }
      }]
    },


    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': ' + tooltipItem.yLabel;
        }
      }
    }
  }
}

var myLineChart = new Chart(ctx, config);


// Fetch data from websocket and update chart

var maxPoints = 20;
var msgCount = 0;

var client = new Paho.MQTT.Client(MQTTbroker, MQTTport,
      "myclientid_" + parseInt(Math.random() * 100, 10));
client.onMessageArrived = onMessageArrived;
client.onConnectionLost = onConnectionLost;

//mqtt connecton options including the mqtt broker subscriptions
var options = {
  timeout: 3,
  onSuccess: function () {
    console.log("mqtt connected");
    // Connection succeeded; subscribe to our topics
    client.subscribe(MQTTsubTopic, {qos: 1});
  },
  onFailure: function (message) {
    console.log("Connection failed, ERROR: " + message.errorMessage);
    //window.setTimeout(location.reload(),20000); //wait 20seconds before trying to connect again.
  }
};

// Connect to MQTT broker
client.connect(options);

//can be used to reconnect on connection lost
function onConnectionLost(responseObject) {
  console.log("connection lost: " + responseObject.errorMessage);
  //window.setTimeout(location.reload(),20000); //wait 20seconds before trying to connect again.
};
//what is done when a message arrives from the broker
function onMessageArrived(message) {
  msgCount++;

  if (msgCount > maxPoints) config.data.datasets[0].data.shift();;

  data = JSON.parse(message.payloadString)
  var val = parseFloat(data.value).toFixed(2)
  config.data.datasets[0].data.push({
    x: data.timestamp,
    y: val
  });
  window.myLineChart.update();

};
