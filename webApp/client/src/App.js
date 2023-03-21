import React from "react";
import logo from "./logo.svg";
import "./App.css";
import * as PIXI from 'pixi.js';
//import './top-view-map.js'; // Import the top-view-map.js file


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

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      msgs: [],
      isLoading: true
    };

    this.app = new PIXI.Application({
      width: 800,
      height: 600,
      backgroundColor: 0x282c34,
      transparent: true
    });

    this.cars = new PIXI.Graphics();
    this.app.stage.addChild(this.cars);

    this.track = new PIXI.Graphics();
    this.app.stage.addChild(this.track);
    document.body.appendChild(this.app.view);


  }

  componentDidMount() {
    this.fetchData();
    this.interval = setInterval(() => {
      this.fetchData();
    }, 500); // Fetch data every 0.5 seconds

    this.interval = setInterval(() => {
      
      fetch("/api/track")
      .then((res) => res.json())
      .then((data) => { 
      console.log(data['track']);

      this.track.clear();
      for(var key in data['track']) {
        var value = data['track'][key];
        let a = value[0]; 
        let b = value[1]; 
        this.track.lineStyle(12, 0x000000);
        this.track.moveTo(a[0], a[1]); 
        this.track.lineTo(b[0], b[1]);
      }
      
      //document.body.appendChild(this.app.view);
      this.forceUpdate();
      });

      fetch("/api/competitors")
      .then((res) => res.json())
      .then((data) => { 
      console.log(data['competitors']);

      this.cars.clear();
      for(var key in data['competitors']) {
        var value = data['competitors'][key];
        let x = value[0]; 
        let y = value[1]; 
        this.cars.lineStyle(12, 0xff0000);
        this.cars.drawCircle(x, y, 10);
        console.log(key, x, y, value)

      
      }
      });
    }, 50);


  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  fetchData = () => {
    fetch("/api/msgs")
      .then((res) => res.json())
      .then((data) => this.setState({ msgs: data['message'], isLoading: false }));
  }

  render() {
    const { msgs, isLoading } = this.state;

    return (
      <div className="App">
        <header className="App-header">
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <ul>
              {msgs.map((message, index) => (
                <li key={index}>{message}</li>
              ))}
            </ul>
          )}
        </header>
      </div>
    );
  }
}

export default App;
