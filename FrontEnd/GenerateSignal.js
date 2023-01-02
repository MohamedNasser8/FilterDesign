const canvas = document.getElementById("drawing-board");
const toolbar = document.getElementById("toolbar");
const ctx = canvas.getContext("2d");

const canvasOffsetX = canvas.offsetLeft;
const canvasOffsetY = canvas.offsetTop;
var graphDiv = document.getElementById("myDiv");
canvas.width = window.innerWidth - canvasOffsetX;
canvas.height = window.innerHeight - canvasOffsetY;

var data = [
  {
    x: [0],
    y: [0],
    mode: "lines",
    line: {
      shape: "spline",
      color: "#febc2c",
    },
  },
];
var layout = {
  yaxis: { range: [-1, 2.5] },
  plot_bgcolor: "#111111",
  paper_bgcolor: "#111111",
};
Plotly.newPlot(graphDiv, data, layout);

let isPainting = false;
let lineWidth = 0;
let startX;
let startY;

toolbar.addEventListener("click", (e) => {
  if (e.target.id === "clear") {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
});

toolbar.addEventListener("change", (e) => {
  if (e.target.id === "color") {
  }
  if (e.target.id === "stroke") {
    ctx.strokeStyle = e.target.value;
  }

  if (e.target.id === "lineWidth") {
    lineWidth = e.target.value;
  }
});
let d0 = new Date();
let t = [0];
let y = [0];
const draw = (e) => {
  if (!isPainting) {
    return;
  }
  const d = new Date();
  realTime(
    d.getMinutes() * 60000 +
      d.getSeconds() * 1000 +
      d.getMilliseconds() -
      (d0.getMilliseconds() + d0.getSeconds() * 1000 + d0.getMinutes() * 60000),
    e.clientY
  );
  //console.log(e.clientX, e.clientY);
  ctx.lineWidth = lineWidth;
  ctx.lineCap = "round";

  ctx.lineTo(e.clientX - canvasOffsetX, e.clientY);
  ctx.stroke();
};

canvas.addEventListener("mousedown", (e) => {
  try {
    console.log(graphDiv.data.length);
  } catch {
    console.log("can not delete traces");
  }
  console.log(Plotly);
  isPainting = true;
  startX = e.clientX;
  startY = e.clientY;

  d0 = new Date();
  console.log("down");
  Plotly.addTraces("myDiv", data);
  console.log(graphDiv.data.length);
});

canvas.addEventListener("mouseup", (e) => {
  isPainting = false;
  Plotly.deleteTraces("myDiv", 0);
  ctx.stroke();
  ctx.beginPath();

  console.log("up");
});
canvas.addEventListener("mousemove", draw);

let cnt = 1;
function realTime(x, y) {
  let update = {
    x: [[x]],
    y: [[y]],
  };
  if (!t[cnt]) {
    t.push(10);
    y.push(10);
  }
  //console.log(y[cnt]);
  let minuteView = {
    xaxis: {
      range: [t[cnt] - 0, y[cnt] - 0],
    },
    yaxis: { rangemode: "tozero", autorange: true },
  };

  Plotly.relayout("myDiv", minuteView);
  Plotly.extendTraces("myDiv", update, [0]);

  cnt++;
  if (cnt === 2000) {
    clearInterval(plotting_interval);
  }
}
