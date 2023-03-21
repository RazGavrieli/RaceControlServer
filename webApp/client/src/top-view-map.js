const PIXI = require('pixi.js');

const app = new PIXI.Application({
  width: 800,
  height: 600,
  backgroundColor: 0x282c34,
});

const carsContainer = new PIXI.Container();
app.stage.addChild(carsContainer);

const track = new PIXI.Graphics();
track.moveTo(3, 5);
track.lineTo(555, 333);
track.lineStyle(2, 0x000000);


app.stage.addChild(track);

class Car extends PIXI.Graphics {
  constructor(id, color) {
    super();
    this.id = id;
    this.color = color;
    this.beginFill(color);
    this.drawCircle(0, 0, 10);
    this.endFill();
  }

  setPosition(X, Y) {
    this.x = X;
    this.y = Y;
  }
}

const carColors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00];
for (let i = 0; i < 4; i++) {
  const car = new Car(i, carColors[i]);
  //car.setPosition(i * 90, 180);
  carsContainer.addChild(car);
}

function update() {
  fetch("/api/track")
  .then((res) => res.json())
  .then((data) => { 
  // let a = data['a']; 
  // let b = data['b']; 
  // track.moveTo(a[0], a[1]); 
  // track.lineTo(b[0], b[1]);
});
  const deltaTime = app.ticker.elapsedMS / 1000;
  carsContainer.children.forEach(car => {
    const speed = 50; // pixels per second
    const angleDelta = speed / 180 * Math.PI * deltaTime;
    car.angle += angleDelta * 180 / Math.PI;
    // GET X AND Y VALUES FROM SERVER
    fetch("/api/competitors")
      .then((res) => res.json())
      .then((data) => { if (data['id'] === car.id) {let x = data['x']; let y = data['y']; car.setPosition(x, y);}});
  });
}


setInterval(() => {
  this.fetchData();
}, 500);
//app.ticker.add(update);

document.body.appendChild(app.view);


